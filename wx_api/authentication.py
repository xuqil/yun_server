from .models import AuthToken
from django.http import HttpResponse
from django.views import View
from .untils import base64_decode


class MyAuthentication(View):
    """
    token认证
    """
    def dispatch(self, request, *args, **kwargs):
        authentication = request.META.get('HTTP_AUTHENTICATION')  # 获取头部信息
        if authentication is None or authentication == '':
            return HttpResponse("error")
        try:
            base64_authentication = str(authentication).split(' ')
            base64_token = base64_authentication[1]
        except IndexError:
            return HttpResponse("格式不符合")
        try:
            request_token = str(base64_decode(base64_token)).split(":")[1]
            uid = str(base64_decode(base64_token)).split(":")[2]
        except IndexError:
            return HttpResponse("authentication格式不正确")
        except ValueError:
            return HttpResponse("authentication格式不正确")
        try:
            user = AuthToken.objects.filter(uid_id=uid).first()
        except ValueError:
            return HttpResponse("userid的值不对，验证失败")
        if user is None:
            return HttpResponse("找不到该用户，验证失败")
        token = user.key
        if token != request_token:
            return HttpResponse("token不正确或者已经过期")
        handler = super(MyAuthentication, self).dispatch(request, *args, **kwargs)
        return handler
