from django.db import models

from addresses.models import Address
from staffs.validators import validate_amharic


class Campus(models.Model):
    name = models.CharField(max_length=255, verbose_name="Campus Name")
    name_am = models.CharField(
        max_length=255, verbose_name="የካምፓስ ስም", validators=[validate_amharic]
    )
    address = models.ForeignKey(
        Address,
        related_name="campus_address",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Department Name")
    name_am = models.CharField(
        max_length=255, verbose_name="የትምህርት ክፍል", validators=[validate_amharic]
    )
    campus = models.ForeignKey(
        Campus, related_name="departments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
