# from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# TOKEN
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser
from djongo import models
import datetime

# Create your models here.
class MyAccountManager(BaseUserManager):
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create_user(self, email, username, user_phone, app_identify, password=None):
        if not email:
            raise ValueError('User Harus Memiliki Email')
        if not username:
            raise ValueError('User Harus Memiliki Username')

        user = self.model(
                email = self.normalize_email(email),
                username = username,
                user_phone = user_phone,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_phone, app_identify, password):
        user = self.create_user(
                email = self.normalize_email(email),
                password=password,
                username = username,
                user_phone = user_phone,
                app_identify = app_identify
            )

        user.is_admin = True
        user.is_staff = True
        user.is_inventory = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Master_User(AbstractBaseUser):
    user_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=30, error_messages={
            'unique': "Username Sudah Pernah Dipakai.",
        })
    email = models.EmailField(verbose_name = 'email', max_length=100, unique=True, error_messages={
            'unique': "Email Sudah Pernah Dipakai.",
        })
    user_phone = models.CharField(max_length=13, error_messages={
            'unique': "No Hp Sudah Pernah Dipakai.",
        })
    user_address = models.TextField()
    is_admin = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verif = models.BooleanField(default=False)
    email_verif_code = models.TextField(default=uuid.uuid4, editable=False, unique=True)
    is_hp_verif = models.BooleanField(default=False)
    hp_verif_code = models.TextField()
    verif_exp_time = models.DateTimeField(default=datetime.datetime.now)
    foto = models.TextField(default = '')
    # bus_id = models.TextField(default = '')
    token_forgot_pwd = models.TextField(default = '')
    forgot_pwd_time_exp = models.DateTimeField(default=datetime.datetime.now)
    created_at = models.DateTimeField(verbose_name = 'created at', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name = 'created at', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_phone']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    class Meta:
        unique_together = ('username', 'email')

class Master_PollingManager(models.Manager):
    def get_active_polling(self):
        return super(Master_PollingManager, self).get_queryset().filter(polling_status = True)

    def get_nonactive_polling(self):
        return super(Master_PollingManager, self).get_queryset().filter(polling_status = False)

    def get_owned_polling(self, request):
        return super(Master_PollingManager, self).get_queryset().filter(polling_creator = request.user)

    def get_active_owned_polling(self, request):
        return super(Master_PollingManager, self).get_queryset().filter(polling_creator = request.user, polling_status = True)
    
    def get_nonactive_owned_polling(self, request):
        return super(Master_PollingManager, self).get_queryset().filter(polling_creator = request.user, polling_status = False)


class Master_Polling(models.Model):
    polling_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    polling_question = models.TextField(editable=False, unique=True)
    polling_choices = JSONField(default=list, null=False, blank=False)
    polling_allow_multiple = models.BooleanField(default=False)
    polling_comment_off = models.BooleanField(default=False)
    polling_exp_date = models.DateTimeField(default=None, null=True)
    polling_creator = models.ForeignKey(Master_User, on_delete=models.PROTECT, null=True)
    polling_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Master_PollingManager() 