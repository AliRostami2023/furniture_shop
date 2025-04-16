from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import PasswordResetToken, Profile

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'password', 'confirm_password']

        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
            'confirm_password': {'required': True, 'write_only': True},
            'phone_number': {'required': True},
            'email': {'required': True},
            'full_name': {'required': True},
        }

    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(_('کاربری در گذشته با این شماره تلفن ثبت نام کرده است!!!'))
        return phone_number
    

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('کاربری در گذشته با این ایمیل ثبت نام کرده است!!!'))
        return email
    

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(_('کلمه عبور و تکرار آن باید یکسان باشد!!!'))
        return attrs
    

class PasswordResetRequestSerializers(serializers.Serializer):
    email = serializers.EmailField()


    def validate_email(self, value):
        email = value.lower().strip()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('کاربری با این ایمیل وجود ندارد !!!'))
        return email



class PasswordResetConfirmSerializers(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs['new_password']
        password2 = attrs['confirm_new_password']

        if password1 and password1 != password2:
            raise serializers.ValidationError(_('کلمه عبور باید یکسان باشد !!!'))
        elif len(password1) < 8:
            raise serializers.ValidationError(_('کلمه عبور باید شامل 8 کاراکتر یا عدد باشد !!!'))
        return attrs


    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(is_used=False, token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_('توکن معتبر نیست'))

        if not reset_token.is_valid():
            raise serializers.ValidationError(_('توکن منقضی شده است'))
        return value


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'email', 'last_login']

        extra_kwargs = {
            'phone_number': {'read_only': True},
            'email': {'read_only': True},
            'last_login': {'read_only': True},
        }


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'brithday', 'address', 'about_me']


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'brithday', 'address', 'about_me']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'brithday', 'address', 'about_me']
