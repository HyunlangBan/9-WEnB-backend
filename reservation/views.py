import json
from datetime               import date, datetime

from django.views           import View
from django.http            import HttpResponse, JsonResponse

# from user.decorator         import login_check
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

class ReservationView(View):
    # @login_check
    def get(self, request):
        user = User.objects.prefetch_related("reservation").get(id=request.user.id)
        current_date = datetime.today().strftime('%Y-%m-%d')
        state = request.GET.get("tab", None)

        reservation_states = {
            "이전 예약": "check_out__lte",
            "예정된 예약": "check_in__gte"
        }
        if state in reservation_states:
            curr_state = reservation_states[state]
            reservation_list = [{
            "name" : reservation.stay.title,
            "location" : reservation.stay.address,
            "stay_date" : str(reservation.check_in.month) + "월 " + str(reservation.check_in.day) + "일 - "+ str(reservation.check_out.month) + "월 " + str(reservation.check_out.day) + "일",
            }for reservation in user.reservation.filter(curr_state = current_date)]
        
            return JsonResponse({"stay_list": reservation_list}, status=200)
            
        return JsonResponse({"message": "invalid tab"}, status=404)