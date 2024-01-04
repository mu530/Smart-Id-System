from django.contrib import admin

from .models import Student, EmergencyContact

admin.site.register(Student)
admin.site.register(EmergencyContact)
