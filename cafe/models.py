import datetime
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

from staffs.validators import validate_amharic
from students.models import Student


class MealPeriod(models.Model):
    meal_period = models.CharField(max_length=20, unique=True)
    meal_period_am = models.CharField(
        "የምግብ ሰዓት", max_length=20, validators=[validate_amharic], unique=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    start_day = models.DateField()
    end_day = models.DateField()

    def __str__(self):
        return self.meal_period

    # def get_absolute_url(self):
    #     return reverse("Cafe:list_meal", kwargs={"pk": self.pk})


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    meal_period = models.ForeignKey(MealPeriod, on_delete=models.CASCADE)
    date_checked = models.DateField(auto_now_add=True)
    time_checked = models.TimeField(null=True, blank=True)
    has_eaten = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.meal_period} - {self.date_checked}"

    def save(self, *args, **kwargs):
        if self.has_eaten:
            self.time_checked = datetime.datetime.now().time()
        super().save(*args, **kwargs)

    @classmethod
    def create_attendance_for_today(cls):
        today = datetime.date.today()
        meals = MealPeriod.objects.filter(start_day__lte=today, end_day__gte=today)
        students = Student.objects.filter(is_cafe_user=True)

        for meal in meals:
            for student in students:
                if not cls.objects.filter(
                    student=student, meal_period=meal, date_checked=today
                ).exists():
                    cls.objects.create(
                        student=student, meal_period=meal, date_checked=today
                    )
