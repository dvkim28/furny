from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_service.utils import send_verification_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password", "is_staff", "is_email_verified"]
        extra_kwargs = {
            "password": {"min_length": 5, "write_only": True},
        }
        read_only_fields = ["id", "is_staff", "is_email_verified"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        send_verification_email(user)
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = validated_data.pop("password", None)
        if password:
            user.set_password(password)
            user.save()
        return user


class ManageUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    is_email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name", "is_staff", "is_email_verified"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return super().update(instance, validated_data)
