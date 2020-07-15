import json
import jwt

from django.test import TestCase
from django.test import Client
from unittest.mock import patch
from user.decorator import login_check
from user.models import (
    User, 
    Host
)
from stay.models import (
    Stay, 
    Tag, 
    BuildingHouseType, 
    BuildingType, 
    HouseType
)
from reservation.models import (
    Reservation, 
    OrderStatus
)
from wenb.settings import (
    SECRET_KEY, 
    ALGORITHM
)

token = jwt.encode( {'user_id': 1}, SECRET_KEY, algorithm = ALGORITHM ).decode('utf-8')

class ReservationTest(TestCase):
    def setUp(self):
        User.objects.create(
                id              = 1,
                nickname        = 'test_user',
                thumbnail_image = 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg',
                is_host         = False,
                email           = 'test@email.com',
                kakao_id        = 12345
                )
        Tag.objects.create(id=1, title="Title1", detail="detail1")
        Host.objects.create(id=1, description="Host1", is_superhost=False)
        BuildingType.objects.create(id=1, name="type1")
        HouseType.objects.create(id=1, name="house1")
        BuildingHouseType.objects.create(
                id            = 1,
                building_type = BuildingType.objects.get(id = 1),
                house_type    = HouseType.objects.get(id = 1)
                )
        OrderStatus.objects.create(id=1, status="Pending")
        OrderStatus.objects.create(id=2, status="Complete")
        Stay.objects.create(
                id             = 1,
                title          = "소길숲속 효리네 민박 옆집",
                address        = '애월읍, 제주시, 제주도, 한국',
                sub_title      = '건용님이 호스팅하는 타운하우스의 개인실',
                price          = 60000.00,
                capacity       = 2,
                bedroom_count  = 1,
                bathroom_count = 1,
                longitude      = 126.373900,
                latitude       = 33.430870,
                tag            = Tag.objects.get(id = 1),
                host           = Host.objects.get(id = 1),
                building_house = BuildingHouseType(id = 1)
                )
        Reservation.objects.create(
                id              = 1,
                check_in        = '2020-10-10',
                check_out       = '2020-10-14',
                one_night_price = 20000,
                service_fee     = 1000,
                occupancy_taxes = 1000,
                total_price     = 22000,
                order_status_id = 1,
                stay_id         = 1,
                user_id         = 1,
                guests          = 2
                )


    def tearDown(self):
        User.objects.all().delete()
        Stay.objects.all().delete()
        Tag.objects.all().delete()
        Host.objects.all().delete()
        BuildingType.objects.all().delete()
        OrderStatus.objects.all().delete()
        BuildingHouseType.objects.all().delete()
        Reservation.objects.all().delete() 

    def test_post_reservation_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token}
        reservation_info = {
                'stay_id'         : 1,
                'guest'           : 2,
                'one_night_price' : 20000,
                'service_fee'     : 1000,
                'occupancy_taxes' : 1400,
                'total_price'     : 22400,
                'check_in'        : '2020-10-22',
                'check_out'       : '2020-10-25'
                }
        response = client.post('/reservation', json.dumps(reservation_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_post_reservation_invalid_keys(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token}
        reservation_info = {
                'stay'            : 1,
                'guest'           : 2,
                'one_night_price' : 20000,
                'service_fee'     : 1000,
                'occupancy_taxes' : 1400,
                'total_price'     : 22400,
                'check_in'        : '2020-10-22',
                'check_out'       : '2020-10-25'
                }
        response = client.post('/reservation', json.dumps(reservation_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_reservation_invalid_token(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': 'token'}
        reservation_info = {
                'stay_id'         : 1,
                'guest'           : 2,
                'one_night_price' : 20000,
                'service_fee'     : 1000,
                'occupancy_taxes' : 1400,
                'total_price'     : 22400,
                'check_in'        : '2020-10-22',
                'check_out'       : '2020-10-25'
                }
        response = client.post('/reservation', json.dumps(reservation_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_reservation_infomation_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token }
        response = client.get('/reservation?reservation_id=1', **header)

        self.assertEqual(response.status_code, 200)

    def test_get_reservation_infomation_invalid_reservation_id(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token }
        response = client.get('/reservation?reservation_id=100', **header)

        self.assertEqual(response.status_code, 400)

    def test_get_reservation_infomation(self):
        client = Client()
        header = { 'HTTP_AUTHORIZATION': token }
        response = client.get('/reservation', **header)

        self.assertEqual(response.status_code, 400)

    def test_patch_reservation_information_success(self):
        client = Client()
        header = { 'HTTP_AUTHORIZATION': token }
        response = client.patch('/reservation?reservation_id=1', **header)
        
        self.assertEqual(response.status_code, 200)

    def test_patch_reservation_invalid_reservation_id(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token }
        response = client.patch('/reservation?reservation_id=100', **header)

        self.assertEqual(response.status_code, 400)

    def test_patch_reservation_invalid_reservation_id(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION': token }
        response = client.patch('/reservation', **header)

        self.assertEqual(response.status_code, 400)

