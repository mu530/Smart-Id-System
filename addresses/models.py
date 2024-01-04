from django.db import models
from staffs.validators import validate_ethiopian_phone_number, validate_amharic


class Address(models.Model):
    phone_number = models.CharField(
        max_length=20,
        validators=[validate_ethiopian_phone_number],
        null=True,
        blank=True,
    )
    email = models.EmailField(null=True, blank=True)
    po_box = models.IntegerField("P.O. Box", null=True, blank=True)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)
    region_am = models.CharField(
        "ክልል", max_length=150, validators=[validate_amharic], null=True, blank=True
    )
    city = models.CharField(max_length=100, null=True, blank=True)
    city_am = models.CharField(
        "ከተማ", max_length=150, validators=[validate_amharic], null=True, blank=True
    )
    wereda = models.CharField(max_length=100, null=True, blank=True)
    wereda_am = models.CharField("ወረዳ", max_length=100, null=True, blank=True)
    kebele = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.country or ''} {self.region or ''} {self.city or ''}"

    def get_address_am(self):
        return f"{self.country or ''} {self.region_am or ''} {self.city_am or ''}"
