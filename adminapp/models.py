from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from decimal import Decimal, ROUND_DOWN
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(_('User ID'), max_length=64, db_index=True, blank=False)
    email = models.EmailField(_('Email Address'), unique=True, db_index=True)
    username = models.EmailField(_('Username'), unique=True, db_index=True)
    first_name = models.CharField(_('First Name'), max_length=250, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=250, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name' ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        '''
        Displays email on admin panel
        '''
        return self.email
