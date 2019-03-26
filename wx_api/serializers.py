from rest_framework import serializers
from wx_api.models import AuthCar


class UserSerializer(serializers.ModelSerializer):
    car_id = serializers.CharField(max_length=10)
    app_id = serializers.CharField(max_length=20)

    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        del validated_data['car_id']
        del validated_data['sms_code']

        user = super().create(validated_data)
        user.save()

    class Meta:
        model = AuthCar
        fields = ('car_id', 'app_id', 'token')
