""""
备注：代码后面需要重构
"""

import json
import time
from PIL import Image
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .untils import Token, md5
from .myquery import query_car
from .authentication import MyAuthentication
from .models import AuthCar, AuthToken, CarComputedDate, CarData, CarImage


def acquire_token(request):
    """
    获取认证token
    """
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
            AuthToken.objects.filter(uid_id=uid).update(key=access_token, update_time=datetime.now())
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
                        "version": "v1"
                    }
                }
            }
        return HttpResponse(json.dumps(context, indent=4))
    else:
        return HttpResponse("error")


class CheckToken(MyAuthentication):
    """
    使用获取的token进行请求(任意请求都需携带)
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse("address-2")

    def post(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def put(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def patch(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def head(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def options(self, request, *args, **kwargs):
        return HttpResponse('address-2')

    def trace(self, request, *args, **kwargs):
        return HttpResponse('address-2')


class ReceiveData(MyAuthentication):
    """
    接收传感器数据
    """
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        gid = data['gid']
        data_record = data['computed']
        print("uid:", self.uid)
        print("gid:", gid, " ", "computed:", data_record)
        list_data = data['list']
        try:
            for g_sid, value in list_data.items():
                print("key:", g_sid)
                car_data_instant = CarData()
                car_data_instant.uid_id = self.uid
                car_data_instant.gid = gid
                car_data_instant.g_sid = g_sid
                car_data_instant.ccd = int(value["ccd"])
                car_data_instant.electric = int(value["electric"])
                car_data_instant.acceleration = int(value["acceleration"])
                car_data_instant.speed = int(value["speed"])
                car_computed_instant = CarComputedDate()
                car_computed_instant.uid_id = self.uid
                car_computed_instant.gid = gid
                car_computed_instant.data_record = data_record
                with transaction.atomic():
                    car_data_instant.save()
                    car_computed_instant.save()
        except Exception as e:
            print("出现错误", e)
            return HttpResponse("error")
        return JsonResponse({
            "code": 201,
            "message": "Successfully Saved.",
            "data": []
        })


class ReceiveImages(MyAuthentication):
    """
    上传图片
    """
    def post(self, request, *args, **kwargs):
        gid = request.POST.get('gid')
        if gid is None:
            return HttpResponse('gid不能为空')
        images = request.FILES
        if images:
            for i in range(len(request.FILES)):
                car_image_instant = CarImage()
                car_image_instant.uid_id = self.uid
                car_image_instant.gid = gid
                car_image_instant.g_sid = i + 1
                image = images.get(str(i + 1))
                image_format = str(image).split('.')[-1]
                # /images_upload/{uid}_{gid}_{g_sid}_{created}
                image_name = '%s.%s' % (str(self.uid) + "_" + str(gid) + "_" + str(i + 1) + "_" +
                                        str(time.time())[:10],
                                        image_format)
                try:
                    img = Image.open(image)
                    img.save('images_upload/' + image_name)
                except OSError:
                    return HttpResponse("图片有误")
                except Exception as e:
                    print(e)
                    return HttpResponse("操作失败")
                with transaction.atomic():
                    car_image_instant.url = 'images_upload/' + image_name
                    car_image_instant.save()
            return JsonResponse({
                "code": 201,
                "message": "Successfully Saved.",
                "data": []
            })
        return HttpResponse('图片为空')


class GetData(MyAuthentication):
    """
    查询图片和数据
    """
    def get(self, request, *args, **kwargs):
        """
        默认分页
        """
        type_ = request.GET.get('type')
        uid = request.GET.get('uid')
        gid = request.GET.get('gid')
        g_sid = request.GET.get('g_sid')
        page = request.GET.get('page')
        # 第几页
        limit = request.GET.get('limit')
        # 每页多少数据
        if page is None:
            page = 1
        if limit is None:
            limit = 10
        if type_ == 'image':
            if uid is None:
                car_image = query_car("CarImage", self.uid, gid, g_sid)
            else:
                car_image = query_car("CarImage", uid, gid, g_sid)
            paginator = Paginator(car_image, int(limit))
            try:
                posts = paginator.page(int(page))
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {"code": 200, "message": "Get image Successfully."}
            data = {}
            list_ = []
            if paginator.count:
                for i in posts.object_list:
                    detail = dict()
                    detail['uid'] = i.uid_id
                    detail['gid'] = i.gid
                    detail['g_sid'] = i.g_sid
                    detail['url'] = str(i.url)
                    # 注意转为字符类型，不然不能序列化
                    detail['create'] = str(i.created)
                    # 注意转为字符类型，不然不能序列化
                    list_.append(detail)
                    data['total'] = paginator.num_pages
                    # 总页数
                    data['page'] = posts.number
                    data['page_size'] = limit
                    data['list'] = list_
                    context['data'] = data
            else:
                context['date'] = {"total": 0, "page": 1, "page_size": limit, "list": [{}]}
            return HttpResponse(json.dumps(context, indent=4))
        elif type_ == 'data':
            if uid is None:
                car_data = query_car("CarData", self.uid, gid, g_sid)
            else:
                car_data = query_car("CarData", uid, gid, g_sid)
            paginator = Paginator(car_data, limit)
            try:
                posts = paginator.page(int(page))
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {"code": 200, "message": "Get image Successfully."}
            data = {}
            list_ = []
            if paginator.count:
                for i in posts.object_list:
                    detail = dict()
                    detail['uid'] = i.uid_id
                    detail['gid'] = i.gid
                    detail['ccd'] = i.ccd
                    detail['electric'] = i.electric
                    detail['acceleration'] = i.acceleration
                    detail['speed'] = i.speed
                    detail['created'] = str(i.created)
                    list_.append(detail)
                    data['total'] = paginator.num_pages
                    data['page'] = posts.number
                    data['page_size'] = limit
                    data['list'] = list_
                    context['data'] = data
            else:
                context['date'] = {"total": 0, "page": 1, "page_size": limit, "list": [{}]}
            return HttpResponse(json.dumps(context, indent=4))
        else:
            return HttpResponse('error')


class GetList(MyAuthentication):
    """
    获取用户列表
    """
    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid')
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        if page is None:
            page = 1
        if limit is None:
            limit = 10
        if uid is None:
            user = AuthCar.objects.all()
            paginator = Paginator(user, limit)
            try:
                posts = paginator.page(int(page))
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {"code": 200, "message": "Get image Successfully."}
            data = {}
            list_ = []
            if paginator.count:
                for i in posts.object_list:
                    detail = dict()
                    detail['uid'] = i.uid
                    detail['carid'] = i.car_id
                    detail['appid'] = i.app_id
                    list_.append(detail)
                    data['total'] = paginator.num_pages
                    data['page'] = posts.number
                    data['page_size'] = limit
                    data['list'] = list_
                    context['data'] = data
            else:
                context['date'] = {"total": 0, "page": 1, "page_size": limit, "list": [{}]}
            return HttpResponse(json.dumps(context, indent=4))
        else:
            user_detail = CarComputedDate.objects.filter(uid_id=uid).order_by('created')
            paginator = Paginator(user_detail, limit)
            try:
                posts = paginator.page(int(page))
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context = {"code": 200, "message": "Get ismage Successfully."}
            data = {}
            list_ = []
            if paginator.count:
                for i in posts.object_list:
                    detail = dict()
                    detail['uid'] = i.uid_id
                    detail['gid'] = i.gid
                    detail['data_record'] = i.data_record
                    detail['data_computed'] = str(i.data_computed)
                    detail['created'] = str(i.created)
                    list_.append(detail)
                    data['total'] = paginator.num_pages
                    data['page'] = posts.number
                    data['page_size'] = limit
                    data['list'] = list_
                    context['data'] = data
            else:
                context['date'] = {"total": 0, "page": 1, "page_size": limit, "list": [{}]}
            return HttpResponse(json.dumps(context, indent=4))


class DeleteCar(MyAuthentication):
    """
    删除数据
    """
    def delete(self, request, type_, uid):
        try:
            uid = int(uid)
        except ValueError:
            uid = uid
        if type_ == 'image':
            try:
                if isinstance(int(uid), int):
                    with transaction.atomic():
                        CarImage.objects.filter(uid_id=uid).all().delete()
            except ValueError:
                if uid == 'all':
                    with transaction.atomic():
                        CarImage.objects.all().delete()
            return HttpResponse("204")
        elif type_ == 'data':
            try:
                if isinstance(int(uid), int):
                    with transaction.atomic():
                        CarData.objects.filter(uid_id=uid).all().delete()
            except ValueError:
                if uid == 'all':
                    with transaction.atomic():
                        CarData.objects.all().delete()
            return HttpResponse("204")
