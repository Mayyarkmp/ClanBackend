import uuid
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from core.base.models import TimeStampedModel
from polymorphic.models import PolymorphicModel, PolymorphicManager


class UserManager(PolymorphicManager, BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **extra_fields):
        if not email and not extra_fields["phone_number"]:
            raise ValueError(
                "Users must have either an email address or a phone number"
            )

        email = self.normalize_email(email) if email else None
        username = (
            username
            if username
            else (
                email.split("@")[0]
                if email
                else (
                    f"user_{uuid.uuid4().hex[:8]}"
                    if email
                    else extra_fields["phone_number"].as_international.replace(" ", "")
                )
            )
        )

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_email_verified = True
        user.polymorphic_ctype = ContentType.objects.get(
            app_label="central_users", model="centraluser"
        )
        user.save()
        return user

    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except:
            ValueError(_("Please enter a valid email address"))


class User(PolymorphicModel, AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    class AuthProviders(models.TextChoices):
        APPLE = "APPLE"
        GOOGLE = "GOOGLE"
        EMAIL = "EMAIL"
        PHONE = "PHONE"

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    email_authentication = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    phone_number_authentication = models.BooleanField(default=False)
    is_phone_number_verified = models.BooleanField(default=False)
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    google_authentication = models.BooleanField(default=False)
    apple_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    apple_authentication = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    tow_factor_authentication = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        return self.email or self.username or self.phone_number.as_international

    @property
    def auth_providers(self):
        providers = []
        if self.email_authentication:
            providers.append("EMAIL")

        if self.phone_number_authentication:
            providers.append("PHONE_NUMBER")

        if self.google_authentication:
            providers.append("GOOGLE")

        if self.apple_authentication:
            providers.append("APPLE")

        return providers

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def link_google_account(self, google_data):
        if not self.google_id:
            self.google_id = google_data["id"]
            self.google_authentication = True
            self.save()
        return self

    def link_apple_account(self, apple_data):
        if not self.apple_id:
            self.apple_id = apple_data["id"]
            self.apple_authentication = True
            self.save()
        return self

    def link_phone_account(self, phone_number):
        if not self.phone_number:
            self.phone_number = phone_number

            self.save()
        return self

    def verified_phone_number(self):
        self.is_verified_phone_number = True
        self.phone_number_authentication = True
        return self

    @property
    def full_name(self):
        if self.last_name is not None:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
        return self

    def __str__(self):
        return self.email or self.username or self.phone_number.as_international
