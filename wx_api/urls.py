from django.urls import path
from wx_api import views, notoken_view
from django.conf.urls.static import static
from django.conf import settings

app_name = 'wx_api'

urlpatterns = [
    # 具有token认证功能的接口
    path('token2', views.acquire_token_overwrite, name='token_overwrite'),
    path('token', views.acquire_token, name='token'),
    path('car/data_token', views.ReceiveData.as_view(), name='receive_data_token'),
    path('car/image_token', views.ReceiveImages.as_view(), name='receive_images_token'),
    path('car_token', views.GetData.as_view(), name='get_data_token'),
    path('user_token', views.GetList.as_view(), name='get_list_token'),
    path('car_token/<str:type_>/<str:uid>', views.DeleteCar.as_view(), name='delete_car_token'),

    # 取消了token认证的接口
    path('car/data', notoken_view.ReceiveData.as_view(), name='receive_data'),
    path('car/image', notoken_view.ReceiveImages.as_view(), name='receive_images'),
    path('car', notoken_view.GetData.as_view(), name='get_data'),
    path('user', notoken_view.GetList.as_view(), name='get_list'),
    path('car/<str:type_>/<str:uid>', notoken_view.DeleteCar.as_view(), name='delete_car'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 图片访问url:http://127.0.0.1:8000/v1/images_upload/2_29_1_1554037928.png
