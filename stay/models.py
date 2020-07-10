from django.db import models

class Stay(models.Model):
    title            = models.CharField(max_length = 100)
    address          = models.CharField(max_length = 100)
    sub_title        = models.CharField(max_length = 50)
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    capacity         = models.IntegerField()
    bedroom_count    = models.IntegerField()
    bathroom_count   = models.IntegerField()
    longitude        = models.DecimalField(max_digits = 10, decimal_places = 6)
    latitude         = models.DecimalField(max_digits = 10, decimal_places = 6)
    tag              = models.OneToOneField('Tag', on_delete = models.SET_NULL, null = True)
    host             = models.ForeignKey('user.Host', on_delete = models.SET_NULL, null = True, related_name  = 'stay')
    building_house   = models.ForeignKey('BuildingHouseType', on_delete = models.SET_NULL, null = True)
    more_stay        = models.ManyToManyField('self', through = 'MoreStay', symmetrical = False)
    wishlist_user    = models.ManyToManyField('user.User', through = 'user.WishList', related_name = 'wishlist_stay')
    reservation_user = models.ManyToManyField('user.User', through = 'reservation.Reservation', related_name = 'reservation_stay')

    class Meta:
        db_table = 'stays'

class Bedroom(models.Model):
    name     = models.CharField(max_length=50, unique = True)
    bed_type = models.ManyToManyField('BedType', through = 'BedroomBedType')

    class Meta:
        db_table = 'bedrooms'

class Image(models.Model):
    image_link = models.URLField(max_length = 200)
    stay       = models.ForeignKey('Stay', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'images'

class MoreStay(models.Model):
    from_stay = models.ForeignKey('Stay', on_delete = models.SET_NULL, null = True, related_name = 'to_stay')
    to_stay   = models.ForeignKey('Stay', on_delete = models.SET_NULL, null = True, related_name = 'from_stay')

    class Meta:
        db_table = 'more_stays'

class BedroomBedType(models.Model):
    bedroom   = models.ForeignKey('Bedroom', on_delete = models.SET_NULL, null = True)
    bed_type  = models.ForeignKey('BedType', on_delete = models.SET_NULL, null = True)
    stay      = models.ForeignKey('Stay', on_delete = models.SET_NULL, null = True)
    bed_count = models.IntegerField()

    class Meta:
        db_table = 'bedrooms_bed_types'

class BedType(models.Model):
    bed_type = models.CharField(max_length=50, unique = True)

    class Meta:
        db_table = 'bed_types'

class Tag(models.Model):
    title  = models.CharField(max_length=100)
    detail = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'tags'

class HouseType(models.Model):
    name          = models.CharField(max_length=50, unique = True)
    building_type = models.ManyToManyField('BuildingType', through = 'BuildingHouseType')

    class Meta:
        db_table = 'house_types'

class BuildingType(models.Model):
    name = models.CharField(max_length=50, unique = True)

    class Meta:
        db_table = 'building_types'

class BuildingHouseType(models.Model):
    building_type = models.ForeignKey('BuildingType', on_delete = models.SET_NULL, null = True)
    house_type    = models.ForeignKey('HouseType', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'building_house_types'

