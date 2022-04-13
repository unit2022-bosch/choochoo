from django.urls import path

from choochoo_app.views import LoadingView

urlpatterns = [
    path("loading", LoadingView.as_view(), name="loading"),
]
