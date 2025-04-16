from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.urls import reverse_lazy
from django.core.mail import send_mail
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .serializers import *
from .models import User, Profile, PasswordResetToken


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data.pop('confirm_password')

        with transaction.atomic():
            User.objects.create_user(**validated_data)

        return Response({'detail': _('ثبت‌نام با موفقیت انجام شد.')}, status=status.HTTP_201_CREATED)
    

class PasswordResetAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetRequestSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email'].lower().strip()
        user = User.objects.get(email=email)
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = request.build_absolute_uri(reverse_lazy('auth:confirm-reset-password', kwargs={'token':str(reset_token.token)}))

        send_mail(
            subject= _('درخواست تغییر کلمه عبور'),
            message= _(f".برای تغییر کلمه عبور روی لینک زیر کلیک کنید {reset_link}"),
            from_email= 'example@gmail.com',
            recipient_list= [user.email],
            fail_silently= False
        )

        return Response({'detail': 'لینک بازیابی رمز عبور ارسال شد.'}, status=status.HTTP_200_OK)




class ConfirmResetPasswordAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetConfirmSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.kwargs['token']
        new_password = serializer.validated_data['new_password']

        reset_token = PasswordResetToken.objects.get(token=token)
        user = reset_token.user

        user.set_password(new_password)
        user.save()

        reset_token.is_used = True
        reset_token.save()

        return Response({'detail': 'رمز عبور با موفقیت تغییر کرد.'}, status=status.HTTP_200_OK)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.select_related('user').get(user=self.request.user)


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.select_related('user').get(user=self.request.user)
    

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = request.data.copy()

        profile.avatar = data.get('avatar', profile.avatar)
        profile.brithday = data.get('brithday', profile.brithday)
        profile.address = data.get('address', profile.address)
        profile.about_me = data.get('about_me', profile.about_me)
        profile.save()

        user_data = data.get('user')
        if user_data:
            user_serializer = UserListSerializer(profile.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    

class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileListSerializer
    permission_classes = [permissions.IsAdminUser]
    