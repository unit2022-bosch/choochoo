from django.db import models
from django.urls import reverse


class Train(models.Model):
    # id is implicit
    human_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Train"
        verbose_name_plural = "Trains"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Train_detail", kwargs={"pk": self.pk})


class Material(models.Model):
    # id is implicit
    material_id = models.CharField(max_length=30, primary_key=True)
    human_name = models.CharField(max_length=255)
    order = models.ForeignKey(
        "choochoo_app.Order", verbose_name=(""), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})


class User(models.Model):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class Station(models.Model):
    # id is implicit
    class Meta:
        verbose_name = "Station"
        verbose_name_plural = "Stations"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Station_detail", kwargs={"pk": self.pk})


class Route(models.Model):
    # id is implicit
    train = models.ForeignKey(
        "choochoo_app.Train", verbose_name=(""), on_delete=models.CASCADE
    )
    station = models.ManyToManyField(Station)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Route_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    # id is implicit
    time = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    station = models.ForeignKey(
        "choochoo_app.Station", verbose_name=(""), on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "choochoo_app.User", verbose_name=(""), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})
