import json
import requests
from time               import strptime
from enum               import Enum
from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Avg
from stay.models        import Stay
from user.models        import User
from reservation.models import (
    OrderStatus, 
    Review, 
    Reservation
)
from user.decorator     import login_check

class ReservationStatus(Enum):
    PROCESSING        = 1
    RESERVED          = 2
    PAYMENT_DONE      = 3
    CANCELED          = 4
    REFUND_PROCESSING = 5
    REFUND_DONE       = 6

class ReservationView(View):
    @login_check
    def post(self, request):
        try:
            res                    = json.loads(request.body.decode("utf-8"))
            stay_id                = res['stay_id']
            guests                 = res['guest']
            one_night_price        = res['one_night_price']
            service_fee            = res['service_fee']
            occupancy_taxes        = res['occupancy_taxes']
            total_price            = res['total_price']
            check_in               = res['check_in'][0:10]
            check_out              = res['check_out'][0:10]
            stay                   = Stay.objects.get(id = stay_id)
            user                   = request.user
            order_status           = OrderStatus.objects.get(id = ReservationStatus.PROCESSING.value)
            reservation_processing = Reservation.objects.create(
                    check_in        = check_in,
                    check_out       = check_out,
                    one_night_price = one_night_price,
                    service_fee     = service_fee,
                    occupancy_taxes = occupancy_taxes,
                    total_price     = total_price,
                    stay            = stay,
                    user            = user,
                    order_status    = order_status,
                    guests          = guests
            )
    
            reservation_id = reservation_processing.id
    
            return JsonResponse({'message':'SUCCESS', 'reservation_id':reservation_id })
        except KeyError:
            return JsonResponse( {'message': 'INAVLID_KEYS'}, status= 400 )


    @login_check
    def get(self, request):
        try:
            reservation_id = request.GET.get('reservation_id', None)
            if reservation_id:
                reservation     = Reservation.objects.get(id  = reservation_id)
                checkin         = reservation.check_in
                checkout        = reservation.check_out
                guests          = reservation.guests
                one_night_price = reservation.one_night_price
                service_fee     = reservation.service_fee
                occupancy_taxes = reservation.occupancy_taxes
                total_price     = reservation.total_price
                stay_title      = reservation.stay.title
                stay_sub_title  = reservation.stay.sub_title
                stay_location   = reservation.stay.address
    
                try:
                    reviews              = Review.objects.filter(reservation_id = reservation.id)
                    review_count         = reviews.count()
                    review_average_score = reviews.annotate(avg = Avg('average_score'))[0].avg

                except IndexError:
                    review_count         = 0
                    review_average_score = 0

                finally:
                    return JsonResponse ( 
                    { 
                        'reservation_id'       : reservation_id,
                        'check_in'             : checkin,
                        'check_out'            : checkout,
                        'guest'                : guests,
                        'one_night_price'      : one_night_price,
                        'service_fee'          : service_fee,
                        'occupancy_taxes'      : occupancy_taxes,
                        'total_price'          : total_price,
                        'stay_title'           : stay_title,
                        'stay_sub_title'       : stay_sub_title,
                        'stay_location'        : stay_location,
                        'review_count'         : review_count,
                        'review_average_score' : review_average_score
                    }, status = 200 )

            return JsonResponse( {'messgae': 'RESERVATION_ID_NONE'}, status=400 )

        except Reservation.DoesNotExist:
            return JsonResponse( {'message': 'INVALID_RESERVATION_ID'}, status = 400)
            
    @login_check
    def patch(self, request):
        reservation_id = request.GET.get('reservation_id', None)
        try:
            if reservation_id:
                reservation                 = Reservation.objects.get(id = reservation_id)
                reservation.order_status_id = ReservationStatus.RESERVED.value
                reservation.save()
    
                return JsonResponse( {'message': 'SUCCESS'}, status=200 )
            return JsonResponse( {'message': 'RESERVATION_ID_NONE'}, status=400 )

        except Reservation.DoesNotExist:
            return JsonResponse( {'message': 'INVALID_RESERVATION_ID'}, status = 400 )
