from datetime import datetime
from datetime import time
from random import choice
from random import randrange

from choochoo_app.models import Train
from django.views.generic import TemplateView

from . import models
from .forms import OrderForm


class LoadingView(TemplateView):
    template_name = "loading/loading.html"

    def get_context_data(self, **kwargs):
        context = super(LoadingView, self).get_context_data(**kwargs)  # mostly useless

        trains = {}
        loading_data = models.Order.get_all_to_load(time(0, 0, 0))
        for route, train, materials in loading_data:
            trains[train.human_id] = {
                "time": route.time,
                "materials": materials.items(),
            }
        context["trains"] = trains

        return context


class StationView(TemplateView):
    template_name = "station/station.html"

    def get_context_data(self, **kwargs):
        context = super(StationView, self).get_context_data(**kwargs)  # mostly useless
        context.update(self.create_context_data(kwargs["station_id"]))
        return context

    def create_context_data(self, station_id, context={}):
        orders = [
            {
                "order_time": datetime.now(),
                "departure_time": datetime.now(),
                "material": randrange(1_000_000_000, 10_000_000_000),
                "amount": randrange(1, 100),
                "id": i,
            }
            for i in range(randrange(10, 30))
        ]

        orders = models.Order.get_orders_for_station(station_id)
        orders_data = [
            {
                "order_time": order.time,
                "departure_time": order.time_of_departure,
                "material": order.material,
                "amount": order.quantity,
            }
            for order in orders
        ]

        context["orders"] = orders_data
        context["form"] = OrderForm()
        context["multiple_warehouses"] = False
        # context["materials"] = [
        #     material.material_id for material in models.Material.objects.all()
        # ]

        return context

    def post(self, request, **kwargs):
        form = OrderForm(request.POST)

        models.Order.create_order(
            kwargs["station_id"],
            request.POST["material"],
            request.POST["amount"],
            datetime.now(),
        ).save()

        return self.get(request, **kwargs)


class LogisticView(TemplateView):
    template_name = "logistics/logistics.html"

    def orders_of_warehouse(self, warehouse):
        return [
            {
                "order_time": datetime.now(),
                "departure_time": datetime.now(),
                "material": randrange(1_000_000_000, 10_000_000_000),
                "amount": randrange(1, 100),
                "id": 1000 * warehouse + i,
            }
            for i in range(randrange(10, 30))
        ]

    def get_context_data(self, **kwargs):
        context = super(LogisticView, self).get_context_data(**kwargs)

        SKLADY = (1, 2, 4, 5)
        orders = []
        for warehouse in SKLADY:
            orders += [
                {"warehouse": warehouse, **order}
                for order in self.orders_of_warehouse(warehouse)
            ]
        orders.sort(key=lambda order: order["order_time"])

        context["orders"] = orders
        context["multiple_warehouses"] = True

        return context
