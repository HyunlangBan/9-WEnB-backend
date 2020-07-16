from django.urls    import path
from .views         import (
    ReservationView,
)
urlpatterns = [
    path('', ReservationView.as_view()),
]