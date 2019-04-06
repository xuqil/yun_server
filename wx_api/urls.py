from django.urls import path
from wx_api import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'wx_api'

urlpatterns = [
    path('token', views.acquire_token, name='token'),
    path('address/2', views.CheckToken.as_view(), name='check_token'),
    path('car/data', views.ReceiveData.as_view(), name='receive_data'),
    path('car/image', views.ReceiveImages.as_view(), name='receive_images'),
    path('car', views.GetData.as_view(), name='get_data'),
    path('user', views.GetList.as_view(), name='get_list'),
    path('car/<str:type_>/<str:uid>', views.DeleteCar.as_view(), name='delete_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 图片访问url:http://127.0.0.1:8000/v1/images_upload/2_29_1_1554037928.png
