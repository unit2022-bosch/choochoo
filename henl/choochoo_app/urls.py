from django.urls import path

from choochoo_app.views import LoadingView, StationView

urlpatterns = [
    path("loading", LoadingView.as_view(), name="loading"),
    path("station", StationView.as_view(), name="station"),
]
