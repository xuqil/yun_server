from rest_framework import serializers
from wx_api.models import AuthCar
from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    car_id = serializers.CharField(max_length=10)
    app_id = serializers.CharField(max_length=20)

    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        del validated_data['car_id']
        del validated_data['sms_code']

        user = super().create(validated_data)
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 对payload部分进行加密
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)  # 生成token

        user.token = token


    class Meta:
        model = AuthCar
        fields = ('car_id', 'app_id', 'token')
