import json


from django.views import View
from django.http            import HttpResponse, JsonResponse
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger

from stay.models    import (
    Stay,
    Bedroom, 
    Image, 
    MoreStay,
    BedroomBedType,
    BedType,
    Tag,
    HouseType,
    BuildingType,
    BuildingHouseType,
)  
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


class ListView(View):
    def get(self, request):
        filters = {}

        stay_type = request.GET.get("stay_type", None)
        price     = request.GET.get("price", None)
        guests    = request.GET.get("guests", None)
        location  = request.GET.get("location", None)

        type_list = ["전체","개인실","객실","다인실"]
        if stay_type:
            if stay_type in type_list:
                filters["building_house__house_type__name"] = stay_type
            else:
                return JsonResponse({"message": "invalid stay_type"}, status=404)

        if price:
            p = price.split("~")
            minimum = p[0]
            maximum = p[1]
            filters['price__gt'] = minimum
            filters['price__lt'] = maximum
        if guests:
            filters['capacity__gte'] = guests
        if location:
            filters["address__contains"] = location
    
        all_stays = Stay.objects.filter(**filters)
        stay_list =[{
            "house_id"              : stay.id,
            "house_name"            : stay.title,
            "house_images"          : [image.image_link for image in stay.image_set.all()],
            "house_address"         : stay.address,
            "house_type"            : stay.sub_title[stay.sub_title.index("하는")+3:],
            "house_capacity"        : stay.capacity,
            "house_num_of_bedroom"  : stay.bedroom_count,
            "house_num_of_bed"      : sum([count["bed_count"] for count in stay.bedroombedtype_set.values("bed_count")]),
            "house_num_of_bathroom" : stay.bathroom_count,
            "house_rating"          : 5.0,
            "house_superhost"       : stay.host.is_superhost,
            "latitude"              : stay.latitude,
            "longitude"             : stay.longitude,
            "price"                 : stay.price,
        }for stay in all_stays]

        page = request.GET.get("page", 1)
        paginator = Paginator(stay_list, 15)

        try:
            stays = paginator.page(page)
        except PageNotAnInteger:
            stays = paginator.page(1)
        except EmptyPage:
            stays = paginator.page(paginator.num_pages)

        page_stay = []
        for index in range(stays.start_index()-1, stays.end_index()):
            if stay_list:
                page_stay.append(stay_list[index])
        return JsonResponse({"stay_list": page_stay}, status=200)
