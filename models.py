from django.db import models


class Train(models.Model):
    # id is implicit
    human_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Train")
        verbose_name_plural = _("Trains")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Train_detail", kwargs={"pk": self.pk})


class Material(models.Model):
    # id is implicit
    human_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})


class Route(models.Model):
    # id is implicit
    train = models.ForeignKey("app.Train", verbose_name=(""), on_delete=models.CASCADE)
    station = models.ForeignKey(
        "app.Station", verbose_name=(""), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Route_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    # id is implicit

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


class User(models.Model):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class Station(models.Model):
    class Meta:
        verbose_name = _("Station")
        verbose_name_plural = _("Stations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Station_detail", kwargs={"pk": self.pk})


class SourceStation(Station):
    ...


class DestinationStation(Station):
    ...
