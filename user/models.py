from django.db import models

class User(models.Model):
    nickname           = models.CharField(max_length=50, unique = True)
    email              = models.EmailField(max_length=200, null = True)
    thumbnail_image    = models.CharField(max_length=200, null = True)
    created_at         = models.DateTimeField(auto_now_add = True)
    is_host            = models.BooleanField()
    host               = models.OneToOneField('Host', on_delete = models.SET_NULL, null = True)
    kakao_id           = models.IntegerField(null = True)

    class Meta:
        db_table = 'users'

class WishList(models.Model):
    user = models.ForeignKey('User', on_delete = models.SET_NULL, null = True)
    stay = models.ForeignKey('stay.Stay', on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'wish_lists'

class Host(models.Model):
    description    = models.TextField()
    is_superhost   = models.BooleanField()
    created_at     = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'hosts'
