from .models import AuthCar, AuthApp, CarComputedDate, CarData, CarImage
from rest_framework.views import APIView


def acquire_token(request):
    if request.method == 'POST':
        uid = request.POST.get("uid")



