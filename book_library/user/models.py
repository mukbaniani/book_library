from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator



class MyUserManager(BaseUserManager):
    def create_user(self, email,  phone, address, last_name, first_name, passport_id, password=None):
        if not email:
            raise ValueError('მეილი აუცილებელია')
        elif not phone:
            raise ValueError('ტელეფონის ნომრის შევსება აუცილებელია')
        elif not address:
            raise ValueError('მისამართი აუცილებელია')
        elif not last_name:
            raise ValueError('გვარი აუცილებელია')
        elif not first_name:
            raise ValueError('სახელი აუცილებელია')
        elif not passport_id:
            raise ValueError('პირადი ნომერი აუცილებელია')
        user = self.model(
            email = self.normalize_email(email),
            phone=phone,
            address=address,
            last_name=last_name,
            first_name=first_name,
            passport_id=passport_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_('მეილი'))
    phone = models.CharField(max_length=30,validators=[], verbose_name=_('ტელეფონის ნომერი'))
    address = models.CharField(max_length=50, verbose_name=_('მისამართი'))
    first_name = models.CharField(max_length=20, verbose_name=_('სახელი'))
    last_name = models.CharField(max_length=25, verbose_name=_('გვარი'))
    passport_id = models.CharField(max_length=11, verbose_name=_('პირადი ნომერი'))


    object = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('მომხმარებელი')

    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)