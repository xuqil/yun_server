from .models import AuthCar, AuthApp, CarComputedDate, CarData, CarImage
from rest_framework.views import APIView



class Token(APIView):
    def post(self, request):
        code = g



