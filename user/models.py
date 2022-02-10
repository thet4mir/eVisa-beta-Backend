from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager


class UserManager(UserManager):
    def get_queryset(self):
        qs = super(UserManager, self).get_queryset().filter(is_deleted=False)
        return qs


class UserManagerAdmin(UserManager):
    def get_queryset(self):
        qs = super(UserManagerAdmin, self).get_queryset()
        return qs


class User(AbstractUser):

    class Meta:
        db_table = "auth_user"

    _objects = UserManagerAdmin()
    objects = UserManager()

    is_deleted = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)


class UserContact(models.Model):

    class Meta:
        db_table = "user_contact"

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_contact')

    phone_no    = models.CharField(max_length=25)
    address     = models.CharField(max_length=2500)
