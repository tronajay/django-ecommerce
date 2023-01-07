from django.db import models
from base.models import BaseModel
from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    mobile_number = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    objects = UserManager()

    def __str__(self):
        return self.email


# Create your models here
class Address(BaseModel):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=13)
    company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email
