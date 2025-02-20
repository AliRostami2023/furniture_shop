from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import CreateUserSerializer, PasswordResetConfirmSerializers, PasswordResetRequestSerializers,\
                            ProfileSerializer
from .models import User, Profile
from .permissions import IsAdminOrSelf


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data).data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"پیغام": "ثبت نام شما با موفقیت انجام شد"}, status.HTTP_201_CREATED)
    

class PasswordResetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetRequestSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('یک ایمیل برای تغییر کلمه عبور برایتان ارسال کردیم!')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ConfirmResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetConfirmSerializers


    def create(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('کلمه عبور با موفقیت تغییر کرد.')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.UpdateModelMixin,
                                                                        viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.select_related('user')
        return Profile.objects.filter(user=self.request.user).select_related('user')
