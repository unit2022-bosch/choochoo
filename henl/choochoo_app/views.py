from django.views.generic import TemplateView
from datetime import datetime


class LoadingView(TemplateView):
    template_name = "loading/loading.html"

    def get_context_data(self, **kwargs):
        context = super(LoadingView, self).get_context_data(**kwargs)  # mostly useless
        data = {
            "id": {"time": datetime.now(), "materials": [("asdsf", 20), ("465435d", 155), ("4354as", 217)]} for _ in range(10)
        }
        context["data"] = data


class StationView(TemplateView):
    template_name = "station/station.html"

    def get_context_data(self, **kwargs):
        context = super(StationView, self).get_context_data(**kwargs)  # mostly useless
        context["bla"] = "to co chci"