from rest_framework import serializers
from django.core.exceptions import ValidationError
import re

from .models import CustomUser
from rest_framework import serializers
from .models import CustomUser, LoginLog


class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False, 'choices': ['user', 'admin']},
        }

    def validate_phone(self, value):
        if value and not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("شماره تلفن نامعتبر است (فرمت: 09xxxxxxxxx).")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.role = validated_data.get('role', 'user')  # پیش‌فرض 'user'
        user.save()
        return user