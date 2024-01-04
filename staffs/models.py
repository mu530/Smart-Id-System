from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .validators import validate_amharic, validate_ethiopian_phone_number


def get_profile_image_filepath(self, image):
    return f"staffs/{self.username}/profile_images/{self.username}_profile_image.png"


def get_default_profile_image():
    return "profile_images/default_profile_pic.png"


class Staff(AbstractUser):
    ROLE = (
        ("REGISTRAR", "Registrar"),
        ("LIBRARIAN", "Librarian"),
        ("PROCTOR", "Proctor"),
        ("SECURITY", "Security"),
        ("CAFE_STAFF", "Cafe Staff"),
        ("ADMIN", "Admin"),
    )
    full_name_am = models.CharField(
        "ሙሉ ስም", max_length=200, validators=[validate_amharic], null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=20,
        validators=[validate_ethiopian_phone_number],
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        "profile picture",
        upload_to=get_profile_image_filepath,
        default=get_default_profile_image,
        blank=True,
    )
    email = models.EmailField("email address", unique=True, null=True, blank=True)
    role = models.CharField("Role", max_length=10, choices=ROLE)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

    def get_absolute_url(self):
        return reverse("Staff:staff_detail", kwargs={"user_id": self.pk})

    def save(self, *args, **kwargs):
        if self.pk is None and self.is_superuser:
            self.role = "ADMIN"
        if self.role in ("ADMIN", "REGISTRAR"):
            self.is_superuser = True
        if self.role not in ("ADMIN", "REGISTRAR"):
            self.is_superuser = False
        if self.photo is None:
            self.photo = get_default_profile_image

        super().save(*args, **kwargs)
