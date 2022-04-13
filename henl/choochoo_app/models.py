from __future__ import annotations
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
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )

    def __str__(self):
        if self.is_in_warehouse:
            return f"Vlak: {self.human_id}, čeká na naložení"
        else:
            return f"Vlak: {self.human_id}, naposledy ve stanici {self.last_station}"

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

    def get_stations(self) -> Set[Station]:
        routes = self.get_routes()
        stations = set()
        for r in routes:
            for s in r.stations:
                stations.add(s)
        return stations

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
    material_id = models.CharField(max_length=30, primary_key=True)
    human_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.material_id}: {self.human_name}"

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


class Route(models.Model):
    # id is implicit
    time = models.TimeField()
    train = models.ForeignKey(
        "choochoo_app.Train", verbose_name=(""), on_delete=models.CASCADE
    )
    stations = models.ManyToManyField(Station)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def get_absolute_url(self):
        return reverse("Route_detail", kwargs={"pk": self.pk})


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
        "choochoo_app.User",
        verbose_name=(""),
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_materials(train: Train, time: int):
        times = train.get_times()
        next_times = sorted(filter(lambda x: x > time, times))
        orders = set(train.get_orders())
        output = []
        for o in orders:  # TODO check for index out of bounds
            if o.time > next_times[0] and o.time < next_times[1]:
                output.append((o.material, o.quantity))
        return output

    @staticmethod
    def create_order(self, station_id, material_id, quantity, time):
        o = Order()
        o.time = time
        o.material = Material.objects.filter(material_id=material_id)[0]
        o.quantity = quantity
        o.station = Station.objects.get(pk=station_id)
        o.user = None
        return o
