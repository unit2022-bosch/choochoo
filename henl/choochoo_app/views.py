from datetime import datetime
from random import choice
from random import randrange

from django.views.generic import TemplateView


class LoadingView(TemplateView):
    template_name = "loading/loading.html"

    def get_context_data(self, **kwargs):
        context = super(LoadingView, self).get_context_data(**kwargs)  # mostly useless
        data = {
            str(i): {
                "time": datetime.now(),
                "materials": [
                    (randrange(1_000_000_000, 10_000_000_000), randrange(1, 100))
                    for _ in range(randrange(20))
                ],
                "name": choice(
                    "Honza Pepa Ivan Vašek Roman Tomáš Radek Hynek Vojta Vítek Kamil".split()
                ),
            }
            for i in range(10)
        }
        context["data"] = data

        return context


class StationView(TemplateView):
    template_name = "station/station.html"

    def get_context_data(self, **kwargs):
        context = super(StationView, self).get_context_data(**kwargs)  # mostly useless
        context["bla"] = "to co chci"

        return context
