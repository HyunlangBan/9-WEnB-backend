from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')), 
    path("stay", include("stay.urls")),
    path('reservations', include('reservation.urls'))
]
