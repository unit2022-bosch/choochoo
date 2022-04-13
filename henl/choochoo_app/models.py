from __future__ import annotations
from typing import List, Set
from django.db import models
from django.urls import reverse


class Station(models.Model):
    # id is implicit
    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"

    def get_absolute_url(self):
        return reverse("Station_detail", kwargs={"pk": self.pk})


class Train(models.Model):
    # id is implicit
    human_id = models.CharField(max_length=255)
    last_station = models.ForeignKey(
        "choochoo_app.Station",
        verbose_name=(""),
        on_delete=models.CASCADE,
        null=True,
    )

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

    def get_stations(self) -> Set[Station]:
        routes = self.get_routes()
        stations = set()
        for r in routes:
            for s in r.stations:
                stations.add(s)
        return stations


class Material(models.Model):
    # id is implicit
    material_id = models.CharField(max_length=30, primary_key=True)
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


class Path(models.Model):
    # id is implicit
    route = models.ForeignKey(
        "choochoo_app.Route", verbose_name=(""), on_delete=models.CASCADE
    )
    source = models.ForeignKey(
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )
    travel_time = models.PositiveSmallIntegerField()


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

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_orders(train: Train) -> Set[Order]:
        relevant_stations = train.get_stations()
        orders = set()
        for s in relevant_stations:
            orders.add(Order.objects.all().filter(station=s))
        return orders

    @staticmethod
    def get_materials(train: Train, time: int):
        times = train.get_times()
        next_times = sorted(filter(lambda x: x > time, times))
        orders = set(Order.get_orders(train))
        output = []
        for o in orders:  # TODO check for index out of bounds
            if o.time > next_times[0] and o.time < next_times[1]:
                output.append((o.material, o.quantity))
        return output
