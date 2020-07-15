import json
from freezegun      import freeze_time

from django.test    import (
    TestCase,
    Client
)
from unittest.mock  import patch, MagicMock

from .models        import (
    Stay,
    Tag,
    BedroomBedType,
    Bedroom,
    BedType,
    Image,
    MoreStay
)
from user.models    import (
    User,
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
