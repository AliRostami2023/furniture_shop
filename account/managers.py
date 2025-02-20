from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, full_name, phone_number, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number, email, full name and password.
        """
        if not phone_number:
            raise ValueError(_('شماره تلفن خود را وارد کنید!'))
        
        if not email:
            raise ValueError(_('ایمیل خود را وارد کنید!'))
        
        if not full_name:
            raise ValueError(_('نام و نام خانوادگی خود را وارد کنید!'))

        user = self.model(
            phone_number=phone_number,
            email=email,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone number, full name, email and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            full_name=full_name,
            email=email
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    