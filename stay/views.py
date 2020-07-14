from django.views import View
from django.http  import JsonResponse

from .models      import Stay

def get_related_stay(stay_list):
    stay_info = [
        {
            "id"                : stay.id,
            "house_name"        : stay.title,
            "house_images"       : stay.image_set.first().image_link,
            "price"             : int(stay.price),
            "house_superhost"   : stay.host.is_superhost, 
        }
        for stay in stay_list
    ]
    return stay_info

def get_bedroom_list(stay_detail):
    bedroom_list = [
        {
            "type" : i.bedroom.name,
            i.bed_type.bed_type : i.bed_count,
        }
        for i in stay_detail.bedroombedtype_set.all()
    ]
    return bedroom_list

class StayDetailView(View):
    def get(self, request, stay_id):
        if Stay.objects.filter(id = stay_id).exists():
            stay_detail = Stay.objects.filter(
                id = stay_id
            ).prefetch_related(
                "image_set",
                "bedroombedtype_set",
                "more_stay",
            ).select_related(
                "tag",
                "host",
                "building_house"
            ).first()
            
            detail        = {
                "id"                             : stay_detail.id,
                "house_name"                     : stay_detail.title,
                "house_address"                  : stay_detail.address,
                "description_title"              : stay_detail.sub_title,
                "house_superhost"                : stay_detail.host.is_superhost,
                "host_name"                      : stay_detail.host.user.nickname,
                "host_created_at"                : stay_detail.host.created_at, 
                "host_description"               : stay_detail.host.description,
                "house_rating"                   : 5.0,
                "house_images"                   : [i.image_link for i in stay_detail.image_set.all()],
                "description_explanation"        : stay_detail.tag.title.split(","),
                "description_explanation_detail" : stay_detail.tag.detail.split(","),
                "price"                          : int(stay_detail.price),
                "house_capacity"                 : stay_detail.capacity,
                "house_num_of_bedroom"           : stay_detail.bedroom_count,
                "house_num_of_bed"               : stay_detail.bedroombedtype_set.first().bed_count,
                "house_num_of_bathroom"          : stay_detail.bathroom_count,
                "longitude"                      : stay_detail.longitude,
                "latitude"                       : stay_detail.latitude,
                "description_explanation_bedtype": get_bedroom_list(stay_detail),
                "review_count"                   : 44,
                "more_stays"                   : get_related_stay([stay.to_stay for stay in stay_detail.to_stay.all()]),

        }
            return JsonResponse(
                {
                    "data":[detail]
                },
                status = 200
            )
        return JsonResponse({"message":"ROOM DOES NOT EXIST"}, status = 400)
