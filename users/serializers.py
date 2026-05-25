from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import CustomUser

class CustomUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            **validated_data
        )
        return user