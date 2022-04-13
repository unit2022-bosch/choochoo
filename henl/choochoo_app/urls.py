from choochoo_app.views import LoadingView
from choochoo_app.views import LogisticView
from choochoo_app.views import StationView
from django.urls import path

urlpatterns = [
    path("loading", LoadingView.as_view(), name="loading"),
    path("station/<int:station_id>", StationView.as_view(), name="station"),
    path("logistics", LogisticView.as_view(), name="logistics"),
]
