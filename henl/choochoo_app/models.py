from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from typing import List, Set
from django.db import models
from django.urls import reverse


class Station(models.Model):
    # id is implicit
    is_warehouse = models.BooleanField()

    def __str__(self):
        if self.is_warehouse:
            return f"Warehouse {self.id}"
        else:
            return f"Station {self.id}"

    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"

    def get_absolute_url(self):
        return reverse("Station_detail", kwargs={"pk": self.pk})


class Train(models.Model):
    # id is implicit
    is_in_warehouse = models.BooleanField()
    human_id = models.CharField(max_length=255)
    last_station = models.ForeignKey(
        "choochoo_app.Station",
        verbose_name=(""),
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        if self.is_in_warehouse:
            return f"Vlak: {self.human_id}, čeká na naložení"
        else:
            return f"Vlak: {self.human_id}, naposledy ve stanici {self.last_station}"

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trains"

    def get_absolute_url(self):
        return reverse("Train_detail", kwargs={"pk": self.pk})

    def get_routes(self) -> List[Station]:
        return self.route_set.all()

    def get_times(self) -> List[int]:
        routes = self.get_routes()
        return sorted([x.time for x in routes])

    @staticmethod
    def trains_to_be_loaded() -> list[Train]:
        return Train.objects.all().filter(is_in_warehouse=True)

    def get_orders(self) -> Set[Order]:
        relevant_stations = self.get_stations()
        orders = set()
        for s in relevant_stations:
            orders.add(Order.objects.all().filter(station=s))
        return orders


class Material(models.Model):
    # id is implicit
    material_id = models.CharField(max_length=30)
    human_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.material_id}: {self.human_name}"

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})

    @staticmethod
    def create(material_id: str, human_name):
        return Material(material_id=material_id, human_name=human_name)


class User(models.Model):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class RouteID(models.Model):
    class Meta:
        verbose_name = "RouteID"
        verbose_name_plural = "RouteIDs"

    def get_absolute_url(self):
        return reverse("RouteID_detail", kwargs={"pk": self.pk})


class PathSegment(models.Model):
    # id is implicit
    route_id = models.ForeignKey(
        "choochoo_app.RouteID",
        verbose_name=(""),
        on_delete=models.CASCADE,
    )
    src = models.ForeignKey(
        "choochoo_app.Station",
        verbose_name=(""),
        on_delete=models.CASCADE,
        related_name="src",
    )
    dst = models.ForeignKey(
        "choochoo_app.Station",
        verbose_name=(""),
        on_delete=models.CASCADE,
        related_name="dst",
    )
    travel_time = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Path"
        verbose_name_plural = "Paths"

    def get_absolute_url(self):
        return reverse("Path_detail", kwargs={"pk": self.pk})


class Route(models.Model):
    # id is implicit
    time = models.DateTimeField()
    train = models.ForeignKey(
        "choochoo_app.Train", verbose_name=(""), on_delete=models.CASCADE
    )
    route_id = models.ForeignKey(
        "choochoo_app.RouteID",
        verbose_name=(""),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def get_absolute_url(self):
        return reverse("Route_detail", kwargs={"pk": self.pk})

    def get_stations(self) -> Set[Station]:
        stations = set()
        for p in self.pathsegment_set.all():
            stations.add(p.src)
        return stations


class Order(models.Model):
    # id is implicit
    time_added = models.DateTimeField()
    time_of_departure = models.DateTimeField()
    quantity = models.PositiveIntegerField()
    material = models.ForeignKey(
        "choochoo_app.Material", verbose_name=(""), on_delete=models.CASCADE
    )
    station = models.ForeignKey(
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "choochoo_app.User",
        verbose_name=(""),
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Objednávka {self.quantity} kusů ({self.material}) na stanici {self.station}"
        )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_all_to_load(time: int):
        assigned_orders = set()
        assigned_routes = set()
        output = []
        for r in Route.objects.all():
            if not r.time >= time:
                continue
            # TODO filter other timeframe
            train: Train = r.train
            if not train.is_in_warehouse:
                continue
            orders = {}
            for s in r.get_stations():
                for o in Order.objects.all().filter(station=s):
                    if o in assigned_orders or o.is_complete:
                        continue
                    assigned_orders.add(o)
                    if o.material not in orders:
                        orders[o.material] = 0
                    orders[o.material] += o.quantity
            output.append((r, train, orders))
        return output

    @staticmethod
    def create_order(station_id, material_id, quantity, time_departure=None):
        o = Order()
        o.time_added = datetime.now()
        if o.time_of_departure is None:
            o.time_of_departure = o.time_added
        o.time_of_departure = time_departure
        o.material = Material.objects.filter(material_id=material_id)[0]
        o.quantity = quantity
        o.station = Station.objects.get(pk=station_id)
        o.user = None
        return o

    @staticmethod
    def get_orders_for_station(station_id):
        return Order.objects.all().filter(station_id=station_id)
