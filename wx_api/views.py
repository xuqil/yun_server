""""
备注：代码后面需要重构
"""
from .models import AuthCar, AuthApp, CarComputedDate, CarData, CarImage, AuthToken
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .untils import Token, md5, base64_decode, base64_encryption
import datetime


@csrf_exempt
def acquire_token(request):
    context = {}
    if request.method == 'POST':
        car_id = request.POST.get('carid')
        app_id = request.POST.get('appid')
        nonce = request.POST.get('nonce')
        timestamp = request.POST.get('timestamp')
        sign = request.POST.get('sign')
        sdasd = request.POST.get('sdasd')
        if car_id is None or app_id is None:
            context = {"error": "1000:Response Invalid"}
            return HttpResponse(json.dumps(context))
        car_id_result = AuthCar.objects.filter(car_id=car_id).first()
        if car_id_result is None:
            AuthCar.objects.create(car_id=car_id, app_id=app_id)
        car_id = AuthCar.objects.filter(car_id=car_id).values('car_id').first()['car_id']
        print('car_id', car_id)
        uid = AuthCar.objects.filter(car_id=car_id).values('uid').first()['uid']
        access_token = AuthToken.objects.filter(uid_id=uid).first()
        key = str(car_id) + str(app_id)
        if access_token is None:
            # 当令牌不存在时
            access_token = Token().generate_token(key=key, timestamp=timestamp)
            AuthToken.objects.create(key=access_token, uid_id=uid)
        access_token = AuthToken.objects.filter(uid_id=uid).values('key').first()['key']
        expires_time = Token().valid_time(access_token)
        if Token().certify_token(key=key, token=access_token, timestamp=timestamp) is False:
            # 令牌过期
            access_token = Token().generate_token(key=key, timestamp=timestamp)
            expires_time = Token().valid_time(access_token)
            AuthToken.objects.filter(uid_id=uid).update(key=access_token, update_time=datetime.datetime.now())
        sign = md5(app_id)

        context = {
                "code": 200,
                "message": "success",
                "data": {
                    "access_token": access_token,
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


@csrf_exempt
def get_base64_token(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHENTICATION')
        print('token', token)
        return HttpResponse('address-2')


