from .models import AuthToken
from django.http import JsonResponse
from django.views import View
from .untils import base64_decode


class MyAuthentication(View):
    """
    token认证
    """
    def dispatch(self, request, *args, **kwargs):
        authentication = request.META.get('HTTP_AUTHENTICATION')  # 获取头部信息
        if authentication is None or authentication == '':
            # authentication不存在
            return JsonResponse({
                'code': 406,
                'msg': 'authentication is None!'
            })
        try:
            base64_authentication = str(authentication).split(' ')
            base64_token = base64_authentication[1]
        except IndexError:
            # authentication格式错误
            return JsonResponse({
                'code': 400,
                'msg': 'Bad Request!'
            })
        try:
            request_token = str(base64_decode(base64_token)).split(":")[1]
            uid = str(base64_decode(base64_token)).split(":")[2]
        except IndexError:
            # authentication格式错误
            return JsonResponse({
                'code': 400,
                'msg': 'Bad Request!'
            })
        except ValueError:
            return JsonResponse({
                'code': 400,
                'msg': 'Bad Request!'
            })
        try:
            user = AuthToken.objects.filter(uid_id=uid).first()
        except ValueError:
            # userid的值不对，验证失败
            return JsonResponse({
                'code': 403,
                'msg': 'Forbidden!'
            })
        if user is None:
            # 找不到该用户，验证失败
            return JsonResponse({
                'code': 403,
                'msg': 'Forbidden!'
            })
        token = user.key
        if token != request_token:
            # token不正确或者已经过期
            print("token过期")
            return JsonResponse({
                "code": 403,
                "msg": "Forbidden!"
            })
        handler = super(MyAuthentication, self).dispatch(request, *args, **kwargs)
        return handler
