from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime
import uuid
import json

from staffs.validators import validate_amharic, validate_birth_date
from addresses.models import Address
from campuses.models import Department
from .utils import generate_qr_code

Staff = get_user_model()


def get_student_photo_filepath(self, image):
    return f"students/{self.full_name()}/photo/{self.full_name()}.png"


def get_default_photo():
    return "profile_images/default_profile_pic.png"


def get_student_qr_code_filepath(self, image):
    return f"student/{self.full_name()}/qr_code/{self.full_name()}.png"


class EmergencyContact(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    full_name_am = models.CharField(
        max_length=255, verbose_name="ሙሉ ስም", validators=[validate_amharic]
    )
    relationship = models.CharField(max_length=255, verbose_name="relationship")
    relationship_am = models.CharField(
        max_length=255, verbose_name="ዝምድና", validators=[validate_amharic]
    )
    address = models.ForeignKey(
        Address, related_name="emergency_adress", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.full_name


class Student(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    # Fields for student information
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    first_name_am = models.CharField(
        max_length=100, verbose_name="ስም", validators=[validate_amharic]
    )
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    last_name_am = models.CharField(
        max_length=100, verbose_name="የአባት ስም", validators=[validate_amharic]
    )
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    photo = models.ImageField(
        upload_to=get_student_photo_filepath, blank=True, default=get_default_photo
    )
    qr_code = models.ImageField(upload_to=get_student_qr_code_filepath, editable=False)
    date_of_birth = models.DateField(validators=[validate_birth_date])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    government_id_number = models.CharField(max_length=50)
    department = models.ForeignKey(
        Department, related_name="students", on_delete=models.RESTRICT
    )
    emergency = models.ForeignKey(EmergencyContact, on_delete=models.RESTRICT)
    registration_date = models.DateTimeField(auto_now_add=True, editable=False)
    address = models.ForeignKey(
        Address,
        related_name="student_address",
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    financial_aid = models.BooleanField()
    is_cafe_user = models.BooleanField(default=True)
    is_student_associative = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def get_absolute_url(self):
        return reverse("Student:profile", kwargs={"id": self.pk})

    def age(self):
        today = datetime.date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_name_am(self):
        return f"{self.first_name_am} {self.last_name_am}"

    def save(self, *args, **kwargs):
        # Generate unique student ID and QR code when student is registered
        if not self.pk:
            # Generate UUID
            unique_id = uuid.uuid4().hex[:5].upper()

            # Get 2 digites of year
            current_year = datetime.datetime.now().year
            last_two_digits = current_year % 100
            year = str(last_two_digits)[-2:]

            # Set student ID in the format "UoG/XXXXX/year"
            self.student_id = f"UoG|{unique_id}|{year}"

            if not self.qr_code:
                student_data = {
                    "student_id": self.student_id,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "first_name_am": self.first_name_am,
                    "last_name_am": self.last_name_am,
                    "campus": self.department.campus.name,
                    "department": self.department.name,
                }
                json_data = json.dumps(student_data)  # Convert data to JSON format
                self.qr_code = generate_qr_code(json_data)
        super().save(*args, **kwargs)


class Device(models.Model):
    DEVICE_TYPE = (("PHONE", "Phone"), ("PC", "PC"))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="devices"
    )
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE)
    device_model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=17)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} ({self.student})"


class DisciplinaryRecord(models.Model):
    # Fields for disciplinary record information
    student = models.ForeignKey(
        Student, related_name="disciplinary_record", on_delete=models.CASCADE
    )
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT)
    reason = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("date",)

    def __str__(self):
        return f"{self.reason} on {self.date.strftime('%Y-%m-%d')}"
