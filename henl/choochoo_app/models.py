from __future__ import annotations
from collections import defaultdict
from typing import List, Set
from django.db import models
from django.urls import reverse


class Station(models.Model):
    # id is implicit
    is_warehouse = models.BooleanField()

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

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trainqs"

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

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})


class User(models.Model):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class PathSegment(models.Model):
    # id is implicit
    route = models.ForeignKey(
        "choochoo_app.Route", verbose_name=(""), on_delete=models.CASCADE
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
    time = models.TimeField()
    train = models.ForeignKey(
        "choochoo_app.Train", verbose_name=(""), on_delete=models.CASCADE
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
    time = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    material = models.ForeignKey(
        "choochoo_app.Material", verbose_name=(""), on_delete=models.CASCADE
    )
    station = models.ForeignKey(
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "choochoo_app.User", verbose_name=(""), on_delete=models.CASCADE
    )
    is_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_all_to_load(time: int):
        assigned_orders = set()
        output = []
        for r in Route.objects.all():
            if not r.time >= time:
                continue
            train: Train = r.train
            if not train.is_in_warehouse:
                continue
            orders = defaultdict(default_factory=0)
            for s in r.get_stations():
                for o in Order.objects.all().filter(station=s):
                    if o in assigned_orders or o.is_complete:
                        continue
                    assigned_orders.add(o)
                    orders[o.material] += o.quantity
            output.append((r, train, orders))
        return output
