from django.urls import path
from wx_api import views

app_name = 'wx_api'

urlpatterns = [
    path('token/', views.acquire_token, name='token'),
    path('address/2/', views.CheckToken.as_view(), name='check_token'),
]
