from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse_lazy
from rest_framework import serializers
from .models import PasswordResetToken, Profile

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'password', 'confirm_password']

        extra_kwargs = {
            'password': {'required': True, 'read_only': True},
            'confirm_password': {'required': True, 'read_only': True},
            'phone_number': {'required': True},
            'email': {'required': True},
            'full_name': {'required': True},
        }

    def validate_phone_number(self, attrs):
        phone_number = attrs.get('phone_number')

        user = User.objects.filter(phone_number=phone_number).exists()

        if user:
            raise serializers.ValidationError(_('کاربری در گذشته با این شماره تلفن ثبت نام کرده است!!!'))
        return user
    

    def validate_email(self, attrs):
        email = attrs.get('email')

        user = User.objects.filter(email=email).exists()

        if user:
            raise serializers.ValidationError(_('کاربری در گذشته با این ایمیل ثبت نام کرده است!!!'))
        return user
    

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(_('کلمه عبور و تکرار آن باید یکسان باشد!!!'))
        return password
    

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)
    

class PasswordResetRequestSerializers(serializers.Serializer):
    email = serializers.EmailField()


    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این ایمیل وجود ندارد !!!'))
        return value
    

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = f"{self.context['request'].build_absolute_uri(reverse_lazy('password-reset', kwargs={'token':str(reset_token.token)}))}"

        send_mail(
            subject= _('درخواست تغییر کلمه عبور'),
            message= _(f"برای تغییر کلمه عبور روی لینک کلیک کنید {reset_link}"),
            from_email= 'example@gmail.com',
            recipient_list= [user.email],
            fail_silently= False
        )

        print(reset_link)
        return reset_token



class PasswordResetConfirmSerializers(serializers.Serializer):
    token = serializers.UUIDField()
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


    def save(self, **kwargs):
        reset_token = PasswordResetToken.objects.get(token=self.validated_data['token'])
        user = reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        reset_token.is_used = True
        reset_token.save()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'email', 'last_login']

        extra_kwargs = {
            'phone_number': {'read_only': True},
            'email': {'read_only': True},
            'last_login': {'read_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'brithday', 'address', 'about_me']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.birthday = validated_data.get('brithday', instance.brithday)
        instance.address = validated_data.get('address', instance.address)
        instance.about_me = validated_data.get('about_me', instance.about_me)
        instance.save()

        if user_data:
            user_serializer = UserListSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        return instance
