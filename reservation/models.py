from django.db import models

class Reservation(models.Model):
    user = models.ForeignKey('user.User', on_delete = models.SET_NULL, null = True, related_name='reservation')
    stay = models.ForeignKey('stay.Stay', on_delete = models.SET_NULL, null = True, related_name='reserved')
    order_status = models.ForeignKey('OrderStatus', on_delete = models.SET_NULL, null = True)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    one_night_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    service_fee = models.DecimalField(max_digits = 10, decimal_places = 2)
    occupancy_taxes = models.DecimalField(max_digits = 10, decimal_places = 2)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        db_table = 'reservations'

class OrderStatus(models.Model):
    status = models.CharField(max_length= 50, unique = True)

    class Meta:
        db_table = 'order_status'

class Review(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete = models.SET_NULL, null = True)
    satisfaction_score = models.IntegerField()
    communication_score = models.IntegerField()
    check_in_score = models.IntegerField()
    cleanliness_score = models.IntegerField()
    accuracy_score = models.IntegerField()
    location_score = models.IntegerField()
    average_score = models.DecimalField(max_digits = 3, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add = True)
    content = models.TextField()

    class Meta:
        db_table = 'reviews'
