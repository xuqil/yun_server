""""
备注：代码后面需要重构
"""
from .models import AuthCar, AuthApp, CarComputedDate, CarData, CarImage, AuthToken
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .untils import Token, md5


@csrf_exempt
def acquire_token(request):
    context = {}
    if request.method == 'POST':
       car_id = request.POST.get('mobile')
       app_id = request.POST.get('appid')
       nonce = request.POST.get('nonce')
       timestamp = request.POST.get('timestamp')
       sign = request.POST.get('sign')
       sdasd = request.POST.get('sdasd')
       if car_id is None or app_id is None:
           context = {"error": "1000:Response Invalid"}
           return HttpResponse(json.dumps(context))
       car_id_result = AuthCar.objects.filter(car_id=car_id).first()
       print("car_id", car_id)
       print("app_id", app_id)
       if car_id_result is None:
           AuthCar.objects.create(car_id=car_id, app_id=app_id)
       car = AuthCar.objects.filter(car_id=car_id).values('car_id').first()
       for i in car.values():
           car_id = i
       uid = AuthCar.objects.filter(car_id=car_id).values('uid').first()
       for i in uid.values():
           uid = i
       access_token = AuthToken.objects.filter(uid_id=uid).first()
       key = str(car_id) + str(app_id)
       if access_token is None:
           # 当令牌不存在时
           access_token = Token().generate_token(key=key, timestamp=timestamp)
           AuthToken.objects.create(key=access_token, uid_id=uid)
       access_token = AuthToken.objects.filter(uid_id=uid).values('key').first()
       access_token_v = None
       for i in access_token.values():
           access_token_v = i
       expires_time = Token().valid_time(access_token_v)
       if Token().certify_token(key=key, token=access_token_v, timestamp=timestamp) is False:
           # 令牌过期
           print("token过期")
           access_token_v = Token().generate_token(key=key, timestamp=timestamp)
           expires_time = Token().valid_time(access_token_v)
           AuthToken.objects.filter(uid_id=uid).update(key=access_token)
       sign = md5(app_id)

       context = {
                "code": 200,
                "message": "success",
                "data": {
                    "access_token": access_token_v,
                    "expires_time": expires_time,
                    "refresh_token": "fmUh89LrwylMd2678ePEciDtYo5Cs7V9",
                    "refresh_expires_time": 1537248112,
                    "client": {
                        "uid": uid,
                        "carid": car_id,
                        "appid": app_id,
                        "nonce": nonce,
                        "timestamp": timestamp,
                        "sign": sign,
                        "sdasd": sdasd,
                        "version": "v1",
                    }
                }
       }
       return HttpResponse(json.dumps(context))
    else:
        return HttpResponse("error")






