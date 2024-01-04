# Generated by Django 4.2.5 on 2023-09-15 11:49

from django.db import migrations, models
import staffs.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_alter_attendance_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealperiod',
            name='meal_period',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='mealperiod',
            name='meal_period_am',
            field=models.CharField(max_length=20, unique=True, validators=[staffs.validators.validate_amharic], verbose_name='የምግብ ሰዓት'),
        ),
    ]