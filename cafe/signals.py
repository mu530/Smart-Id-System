from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from datetime import date

from students.models import Student
from .models import MealPeriod, Attendance


@receiver(post_save, sender=Student)
def create_meal_card(sender, instance, created, **kwargs):
    if created and instance.is_cafe_user:
        meals = MealPeriod.objects.filter(
            start_day__lte=date.today(), end_day__gte=date.today()
        )
        for meal in meals:
            Attendance.objects.create(student=instance, meal_period=meal)


@receiver(pre_delete, sender=Student)
def create_meal_card(sender, instance, **kwargs):
    if instance.is_cafe_user:
        attendence = Attendance.objects.filter(student=instance)
        attendence.delete()


@receiver(post_save, sender=MealPeriod)
def create_meal_card(sender, instance, created, **kwargs):
    if created:
        current_cafe_users = Student.objects.filter(is_cafe_user=True, is_active=True)

        for student in current_cafe_users:
            Attendance.objects.create(student=student, meal_period=instance)


@receiver(pre_delete, sender=MealPeriod)
def create_meal_card(sender, instance, **kwargs):
    attendence = Attendance.objects.filter(meal_period=instance)
    attendence.delete()


@receiver(pre_save, sender=Student)
def update_meal_card(sender, instance, **kwargs):
    try:
        original_student = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed yet
        pass
    else:
        # Check if is_active or is_cafe_user field has changed
        if (
            not original_student.is_active
            and instance.is_active
            and instance.is_cafe_user
        ) or (original_student.is_cafe_user != instance.is_cafe_user):
            # Student has changed from inactive to active and is a cafe user, or is_cafe_user field has changed
            if instance.is_cafe_user and instance.is_active:
                meals = MealPeriod.objects.all()
                for meal in meals:
                    if not Attendance.objects.filter(
                        student=instance, meal=meal
                    ).exists():
                        Attendance.objects.create(student=instance, meal=meal)
            else:
                Attendance.objects.filter(
                    student=instance,
                    meal__meal_period__in=["breakfast", "lunch", "dinner"],
                ).delete()

        if original_student.is_active and not instance.is_active:
            Attendance.objects.filter(
                student=instance,
            ).delete()
