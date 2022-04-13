from django.contrib import admin

from choochoo_app.models import Material, Train, Station, Order


# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
