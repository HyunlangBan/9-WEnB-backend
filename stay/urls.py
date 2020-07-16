from django.urls import path

from .views         import (
    ListView,
    StayDetailView
)

urlpatterns = [
    path("/<int:stay_id>", StayDetailView.as_view()),
    path('', ListView.as_view()),
]
