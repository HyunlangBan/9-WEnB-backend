import json

from django.test            import TestCase
from django.test            import Client
from unittest.mock          import patch, MagicMock
from django.db              import models

from reservation.models     import (
    Reservation,
    OrderStatus,
    Review,
)

from user.models            import (
    User,
    WishList,
    Host,
)
from stay.models            import (
    Stay,
    Bedroom,
    Image,
    MoreStay,
    BedroomBedType,
    BedType,
    Tag,
    HouseType,
    BuildingType,
    BuildingHouseType
)

class ReservationTest(TestCase):
    def setUp(self):
        client = Client()

        User.objects.create(
            id = 1,
            nickname = "jack", 
            is_host = True, 
            email = "jack12@gmail.com"
        )
        Stay.objects.create(
            id               = 1,
            title            = "Jeju hotel",
            address          = "Jeju Island",
            sub_title        = "best hotel",
            price            = 20000,
            capacity         = 3,
            bedroom_count    = 2,
            bathroom_count   = 2,
            longitude        = 20.5,
            latitude         = 22.6
        )
        Reservation.objects.create(
            id = 1,
            user = User.objects.get(id=1),
            stay = Stay.objects.get(id=1),
            one_night_price = 1000,
            service_fee = 100,
            occupancy_taxes = 150,
            total_price = 1150,
            check_in = "2000-01-01",
            check_out = "2000-01-02"
        )
    def tearDown(self):
        Stay.objects.all().delete()
        Reservation.objects.all().delete()
        User.objects.all().delete()

    def test_get_success(self):
        client = Client()
        response = client.get('/reservations?tab=이전 예약')
        self.assertEqual(response.json(),
            {
                "stay_list": [
                    {
                        "name": "Jeju hotel",
                        "location": "Jeju Island",
                        "stay_date": "1월 1일 - 1월 2일"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)  

    def test_url_fail(self):
        client = Client()
        response = client.get('/reservationsss')
        self.assertEqual(response.status_code, 404)

    def test_filter_fail(self):
        client = Client()
        response = client.get('/reservations?tab=이예약')
        self.assertEqual(response.json(),
            {
                "message": "invalid tab"
            }
        )
        self.assertEqual(response.status_code, 404)