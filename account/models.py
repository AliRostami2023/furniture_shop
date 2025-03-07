from django.db import models
import uuid
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from core.models import CreateMixin, UpdateMixin
from .validators import MobileValidator, validate_avatar_size


class User(AbstractBaseUser, PermissionsMixin, CreateMixin, UpdateMixin):
    full_name = models.CharField(max_length=300, verbose_name=_('نام و نام خانوادگی'))
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('شماره تلفن'), validators=[MobileValidator()])
    email = models.EmailField(max_length=300, unique=True, verbose_name=_('ایمیل'))
    is_active = models.BooleanField(default=True, verbose_name=_('فعال'))
    is_admin = models.BooleanField(default=False, verbose_name=_('ادمین'))
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self) -> str:
        return f'{self.phone_number} - {self.full_name}'


    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(CreateMixin, UpdateMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('کاربر'))
    avatar = models.ImageField(upload_to="images/avatar_user", null=True, blank=True, validators=[validate_avatar_size], verbose_name=_('عکس پروفایل'))
    brithday = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('آدرس'))
    about_me = models.TextField(_('درباره من'), null=True, blank=True)

    def __str__(self):
        return self.user.full_name


    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل کاربران')


class PasswordResetToken(CreateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset', verbose_name=_('کاربر'))
    token = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name=_('توکن'))
    is_used = models.BooleanField(default=False, verbose_name=_('استفاده شده'))


    def is_valid(self):
        return datetime.now() > self.create_at + timedelta(days=2) and not self.is_used
    
    def __str__(self):
        return f"{self.user.full_name} - {self.token}"
    
    class Meta:
        verbose_name = _('تغییر کلمه عبور')
        verbose_name_plural = _('توکن های تغییر کلمه عبور')
