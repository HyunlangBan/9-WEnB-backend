import json
from freezegun      import freeze_time

from django.test    import (
    TestCase,
    Client
)
from unittest.mock  import patch, MagicMock
from django.db              import models

from .models        import (
    Stay,
    Tag,
    BedroomBedType,
    Bedroom,
    MoreStay,
    BedType,
    Image,
    MoreStay,
    HouseType,
    BuildingType,
    BuildingHouseType
)
from user.models    import (
    User,
    WishList,
    Host
)

        
TestCase.maxDiff = None

@freeze_time("2020-07-10T08:24:46.562Z")
class StayDetailTest(TestCase):

    def setUp(self):
        client = Client()
        host_ = Host.objects.create(
            id          = 1,
            description = "Hi",
            is_superhost= True,
        )
        user_ = User.objects.create(
            id          = 1,
            nickname    = "monsterkos",
            is_host     = True,
            host        = host_,
        )
        tag_ = Tag.objects.create(
            id              = 1,
            title           = "test",
            detail          = "test_detail"
        )
        stay_ = Stay.objects.create(
            id              = 1,
            title           = "'소길숲속' 효리네 민박 옆집",
            address         = "대한민국 제주시",
            sub_title       = "일단 드루와",
            price           = 1000000,
            capacity        = 2,
            bedroom_count   = 1,
            bathroom_count  = 4,
            longitude       = 10.2,
            latitude        = 49.1,
            tag             = tag_,
            host            = host_,
        )
        bed_type = BedType.objects.create(
            id       = 1,
            bed_type = "킹 사이즈"
        )
        bedroom = Bedroom.objects.create(
            id       = 1,
            name     = "침실",
        )
        bedroom_bed = BedroomBedType.objects.create(
            id         = 1,
            bedroom    = bedroom,
            bed_type   = bed_type,
            stay       = stay_,
            bed_count  = 1,
        )
        image_ = Image.objects.create(
            id         = 1,
            image_link = "www.naver.com",
            stay       = stay_
        )
        MoreStay.objects.create(
            id         = 1,
            from_stay  = stay_,
            to_stay    = stay_,
        )

    def tearDown(self):
        Stay.objects.all().delete()
        User.objects.all().delete()
        Host.objects.all().delete()
        Tag.objects.all().delete()
        BedType.objects.all().delete()
        Bedroom.objects.all().delete()
        BedroomBedType.objects.all().delete()
        Image.objects.all().delete()
        MoreStay.objects.all().delete()

    def test_staydetailview_get_succ(self):
        client = Client()
        response = client.get("/stay/1", content_type = "application/json")
        print(response.json())
        self.assertEqual(response.json(),
            {
                "data"  : [
                    {
                        'id'                            : 1, 
                        'house_name'                    : "'소길숲속' 효리네 민박 옆집", 
                        'house_address'                 : '대한민국 제주시', 
                        'description_title'             : '일단 드루와', 
                        'house_superhost'               : True,
                        'host_name'                     : 'monsterkos', 
                        'host_created_at'               : '2020-07-10T08:24:46.562Z', 
                        'host_description'              : 'Hi', 
                        'house_rating'                  : 5.0, 
                        'house_images'                  : ['www.naver.com'], 
                        'description_explanation'       : ['test'], 
                        'description_explanation_detail': ['test_detail'], 
                        'price'                         : 1000000, 
                        'house_capacity'                : 2, 
                        'house_num_of_bedroom'          : 1, 
                        'house_num_of_bed'              : 1, 
                        'house_num_of_bathroom'         : 4, 
                        'longitude'                     : '10.200000', 
                        'latitude'                      : '49.100000', 
                        'description_explanation_bedtype': [{'type': '침실', '킹 사이즈': 1}],
                        'review_count'                  : 44,
                        'more_stays': [
                            {
                                'id': 1, 
                                'house_name'     : "'소길숲속' 효리네 민박 옆집", 
                                'house_images'   : 'www.naver.com', 
                                'price'          : 1000000, 
                                'house_superhost': True, 
                            }
                        ]
                    }
                ]            
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_staydetailview_get_fail(self):
        client = Client()
        response = client.get("/stay/77")
        self.assertEqual(response.json(),
            {
                "message" : "ROOM DOES NOT EXIST"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_staydetailview_get_not_found(self):
        client = Client()
        response = client.get("/stay/abc")
        self.assertEqual(response.status_code, 404)

class StayTest(TestCase):
    maxDiff = None
    def setUp(self):
        client = Client()

        Host.objects.create(
            id           = 1,
            description  = "여기로오세요", 
            is_superhost = True, 
        )
        HouseType.objects.create(
            id   = 1,
            name = "개인실"
        )
        HouseType.objects.create(
            id   = 2,
            name = "객실"
        )
        HouseType.objects.create(
            id   = 3,
            name = "다인실"
        )
        HouseType.objects.create(
            id   = 4,
            name = "전체"
            )
        BuildingType.objects.create(
            id   = 1,
            name = "타운하우스"
        )
        BuildingType.objects.create(
            id   = 2,
            name = "호텔"
        )
        BuildingType.objects.create(
            id   = 3,
            name = "집"
        )
        BuildingType.objects.create(
            id   = 4,
            name = "아파트"
        )
        
        BuildingHouseType.objects.create(
            id              = 1,
            building_type   = BuildingType.objects.get(id=4),
            house_type      = HouseType.objects.get(id=4)
        )
        BuildingHouseType.objects.create(
            id              = 2,
            building_type   = BuildingType.objects.get(id=4),
            house_type      = HouseType.objects.get(id=4)
        )
        BuildingHouseType.objects.create(
            id              = 3,
            building_type   = BuildingType.objects.get(id=2),
            house_type      = HouseType.objects.get(id=2)
        )
        BuildingHouseType.objects.create(
            id              = 4,
            building_type   = BuildingType.objects.get(id=1),
            house_type      = HouseType.objects.get(id=3)
        )
        Stay.objects.create(
            id               = 1,
            title            = "Jeju hotel",
            address          = "Jeju Island",
            sub_title        = "민서님이 호스팅하는 아파트의 전체",
            price            = 20000,
            capacity         = 3,
            bedroom_count    = 2,
            bathroom_count   = 2,
            longitude        = 20.5,
            latitude         = 22.6,
            host             = Host.objects.get(id = 1),
            building_house   = BuildingHouseType.objects.get(id=1)
        )
        Stay.objects.create(
            id               = 2,
            title            = "Busan Hotel",
            address          = "Busan",
            sub_title        = "민서님이 호스팅하는 집의 전체",
            price            = 30000,
            capacity         = 1,
            bedroom_count    = 2,
            bathroom_count   = 3,
            longitude        = 40,
            latitude         = 50,
            host             = Host.objects.get(id = 1),
            building_house   = BuildingHouseType.objects.get(id=2)
        )
        Stay.objects.create(
            id               = 3,
            title            = "Seoul Hotel",
            address          = "Seoul",
            sub_title        = "민서님이 호스팅하는 호텔의 객실",
            price            = 50000,
            capacity         = 2,
            bedroom_count    = 2,
            bathroom_count   = 2,
            longitude        = 100,
            latitude         = 20,
            host             = Host.objects.get(id = 1),
            building_house   = BuildingHouseType.objects.get(id=3)
        )
        Stay.objects.create(
            id               = 4,
            title            = "New York hotel",
            address          = "New York",
            sub_title        = "민서님이 호스팅하는 타운하우스의 개인실",
            price            = 70000,
            capacity         = 1,
            bedroom_count    = 1,
            bathroom_count   = 1,
            longitude        = 10,
            latitude         = 20,
            host             = Host.objects.get(id = 1),
            building_house   = BuildingHouseType.objects.get(id=4)
        )


    def tearDown(self):
        Stay.objects.all().delete()

    def test_all_stays(self):
        client = Client()
        response = client.get('/stay')
        self.assertEqual(response.json(),
            {
                "stay_list": [
                    {
                        "house_id"                : 1,
                        'house_images'            : [],
                        "house_name"              : "Jeju hotel",
                        "house_address"           : "Jeju Island",
                        "house_type"              : "아파트의 전체",
                        "price"                   : '20000.00',
                        "house_capacity"          : 3,
                        "house_num_of_bedroom"    : 2,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 2,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : '20.500000',
                        "latitude"                : "22.600000"
                    },
                    {
                        "house_id"                : 2,
                        'house_images'            : [],
                        "house_name"              : "Busan Hotel",
                        "house_address"           : "Busan",
                        "house_type"              : "집의 전체",
                        "price"                   : "30000.00",
                        "house_capacity"          : 1,
                        "house_num_of_bedroom"    : 2,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 3,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : "40.000000",
                        "latitude"                : "50.000000"
                    },
                    {
                        "house_id"                : 3,
                        'house_images'            : [],
                        "house_name"              : "Seoul Hotel",
                        "house_address"           : "Seoul",
                        "house_type"              : "호텔의 객실",
                        "price"                   : "50000.00",
                        "house_capacity"          : 2,
                        "house_num_of_bedroom"    : 2,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 2,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : "100.000000",
                        "latitude"                : "20.000000"
                    },
                    {
                        "house_id"                : 4,
                        'house_images'            : [],
                        "house_name"              : "New York hotel",
                        "house_address"           : "New York",
                        "house_type"              : "타운하우스의 개인실",
                        "price"                   : "70000.00",
                        "house_capacity"          : 1,
                        "house_num_of_bedroom"    : 1,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 1,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : "10.000000",
                        "latitude"                : "20.000000"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200) 

    def test_filter_stays(self):
        client = Client()
        response = client.get('/stay?stay_type=전체')
        self.assertEqual(response.json(),
            {
                "stay_list": [
                    {
                        "house_id"                : 1,
                        'house_images'            : [],
                        "house_name"              : "Jeju hotel",
                        "house_address"           : "Jeju Island",
                        "house_type"              : "아파트의 전체",
                        "price"                   : '20000.00',
                        "house_capacity"          : 3,
                        "house_num_of_bedroom"    : 2,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 2,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : '20.500000',
                        "latitude"                : "22.600000"
                    },
                    {
                        "house_id"                : 2,
                        'house_images'            : [],
                        "house_name"              : "Busan Hotel",
                        "house_address"           : "Busan",
                        "house_type"              : "집의 전체",
                        "price"                   : "30000.00",
                        "house_capacity"          : 1,
                        "house_num_of_bedroom"    : 2,
                        'house_num_of_bed'        : 0,
                        "house_num_of_bathroom"   : 3,
                        "house_rating"            : 5.0,
                        "house_superhost"         : True,
                        "longitude"               : "40.000000",
                        "latitude"                : "50.000000"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200) 

    def test_url_fail(self):
        client = Client()
        response = client.get('/staysss')
        self.assertEqual(response.status_code, 404)

        

    def test_location_filter_fail(self):
        client = Client()
        response = client.get('/stay?stay_type=dkjfsl')
        self.assertEqual(response.json(),
            {
                "message": "invalid stay_type"
            }
        )
        self.assertEqual(response.status_code, 404)
    
