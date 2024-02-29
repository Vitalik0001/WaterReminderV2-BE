from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )
    ACTIVITY_CHOICES = (
        ("M", _("Minimal")),
        ("L", _("Low")),
        ("A", _("Average")),
        ("H", _("High")),
        ("V", _("Very high")),
    )
    GENDER_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
    )
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES)
    name = models.CharField(_("name"), max_length=30)
    age = models.IntegerField(
        _("age"), validators=[MinValueValidator(5), MaxValueValidator(120)]
    )
    weight = models.FloatField(
        _("weight"), validators=[MinValueValidator(25.0), MaxValueValidator(200.0)]
    )
    height = models.IntegerField(
        _("height"), validators=[MinValueValidator(100), MaxValueValidator(220)]
    )
    activity = models.CharField(_("activity"), max_length=1, choices=ACTIVITY_CHOICES)
