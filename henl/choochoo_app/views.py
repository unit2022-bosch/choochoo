from datetime import datetime, time
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
        trains = {
            choice(
                "Honza Pepa Ivan Vašek Roman Tomáš Radek Hynek Vojta Vítek Kamil".split()
            ): {
                "time": datetime.now(),
                "materials": [
                    (randrange(1_000_000_000, 10_000_000_000), randrange(1, 100))
                    for _ in range(randrange(1, 20))
                ],
            }
            for i in range(10)
        }

        trains_to_load = Train.trains_to_be_loaded()
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
        orders = [
            {
                "order_time": datetime.now(),
                "departure_time": datetime.now(),
                "material": randrange(1_000_000_000, 10_000_000_000),
                "amount": randrange(1, 100),
            }
            for _ in range(randrange(10, 30))
        ]
        context["orders"] = orders
        context["form"] = OrderForm()
        context["materials"] = [
            material.material_id for material in models.Material.objects.all()
        ]

        return context

    def post(self, request, **kwargs):
        form = OrderForm()
        amount = int(request.POST["amount"])
        material = request.POST["material"]
        models.Order.create_order(kwargs["station_id"], material, amount, 0).save()

        return self.get(request, **kwargs)


class LogisticView(TemplateView):
    template_name = "logisticss/logistics.html"

    def temp(self):
        context = {}
        orders = [
            {
                "order_time": datetime.now(),
                "departure_time": datetime.now(),
                "material": randrange(1_000_000_000, 10_000_000_000),
                "amount": randrange(1, 100),
            }
            for _ in range(randrange(10, 30))
        ]
        context["orders"] = orders
        context["form"] = OrderForm()

        return context

    def get_context_data(self, **kwargs):
        context = super(LoadingView, self).get_context_data(**kwargs)

        SKLADY = (1, 2, 4, 5)
        for warehouse in SKLADY:
            context[warehouse] = self.temp()

        return context
