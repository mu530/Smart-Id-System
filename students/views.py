from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from staffs.decorators import role_required
from addresses.forms import AddressForm
from students.models import DisciplinaryRecord, Student

from .filters import StudentFilter
from .forms import EmergencyContactForm, StudentForm, DeviceForm, DisciplinaryRecordForm


def paginate(request, data, per_page=10):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
@role_required(["REGISTRAR"])
def student_register(request):
    if request.method == "POST":
        student_address_form = AddressForm(request.POST, prefix="student")
        emergency_address_form = AddressForm(request.POST, prefix="emergency")
        emergency_form = EmergencyContactForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)

        if (
            student_address_form.is_valid()
            and student_address_form.is_valid()
            and student_form.is_valid()
            and emergency_form.is_valid()
        ):
            student_address = student_address_form.save()
            emergency_address = emergency_address_form.save()

            emergency = emergency_form.save(commit=False)
            emergency.address = emergency_address
            emergency.save()
            student = student_form.save(commit=False)
            student.address = student_address
            student.emergency = emergency
            student.save()

            return redirect("Student:student_list")
    else:
        student_address_form = AddressForm(prefix="student")
        emergency_address_form = AddressForm(prefix="emergency")

        emergency_form = EmergencyContactForm()

        student_form = StudentForm()

    context = {
        "student_address_form": student_address_form,
        "emergency_address_form": emergency_address_form,
        "student_form": student_form,
        "emergency_form": emergency_form,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "student/student_register.html", context)


@login_required
@role_required(["REGISTRAR"])
def update_student_profile(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == "POST":
        student_address_form = AddressForm(
            request.POST, instance=student.address, prefix="student"
        )
        emergency_address_form = AddressForm(
            request.POST, prefix="emergency", instance=student.emergency.address
        )
        emergency_form = EmergencyContactForm(request.POST, instance=student.emergency)
        student_form = StudentForm(request.POST, request.FILES, instance=student)

        if (
            student_form.is_valid()
            and emergency_form.is_valid()
            and student_address_form.is_valid()
            and emergency_address_form.is_valid()
        ):
            student_address = student_address_form.save()
            emergency_address = emergency_address_form.save()

            emergency = emergency_form.save(commit=False)
            emergency.address = emergency_address
            emergency.save()

            student = student_form.save(commit=False)
            student.address = student_address
            student.emergency = emergency
            student.save()

            return redirect("Student:student_list")
    else:
        student_address_form = AddressForm(instance=student.address, prefix="student")
        emergency_address_form = AddressForm(
            prefix="emergency", instance=student.emergency.address
        )
        emergency_form = EmergencyContactForm(instance=student.emergency)
        student_form = StudentForm(instance=student)

    context = {
        "student_address_form": student_address_form,
        "emergency_address_form": emergency_address_form,
        "student_form": student_form,
        "emergency_form": emergency_form,
        "student": student,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "student/student_update.html", context)


@login_required
def student_profile(request, id):
    student = get_object_or_404(Student, pk=id)
    disciplinary_records = student.disciplinary_record.all()
    print(disciplinary_records)

    devices = student.devices.all()
    disciplinary_records = paginate(request, disciplinary_records, 5)

    context = {
        "student": student,
        "devices": devices,
        "current_url": request.build_absolute_uri(),
        "disciplinary_records": disciplinary_records,
    }

    return render(request, "student/student_profile.html", context)


@login_required
def students_list(request):
    students = Student.objects.all()

    if request.method == "GET":
        sort_by = request.GET.get("sort_by", "")
        if sort_by in ("first_name", "department"):
            students = students.order_by(sort_by)
    student_filter = StudentFilter(request.GET, queryset=students)
    students = student_filter.qs

    # Paginate students
    students = paginate(request, students)

    context = {
        "students": students,
        "student_filter": student_filter,
        "page": "Students_list",
        "page_title": "Students",
        "current_url": request.build_absolute_uri(),
    }
    return render(request, "student/students_list.html", context)


@login_required
def id_card(request, id):
    student = None
    if id is not None:
        student = Student.objects.get(pk=id)

    if request.method == "GET":
        student_id = request.GET.get("student_id", None)

    if student_id:
        student_id = student_id.strip()
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            student = None

    context = {
        "student": student,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "student/student_id.html", context)


@login_required
@role_required(["REGISTRAR"])
def add_device(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        form = DeviceForm(request.POST)

        if form.is_valid():
            device = form.save(commit=False)
            device.student = student
            device.save()

            return redirect("Student:profile", id=student.id)

    else:
        form = DeviceForm()

    return render(
        request, "student/add_device.html", {"form": form, "student": student}
    )


@login_required
def add_disciplinary_record(request, id):
    current_url = request.build_absolute_uri()
    form = DisciplinaryRecordForm
    student = get_object_or_404(Student, pk=id)
    next_page = request.GET.get("next_page")

    if request.method == "POST":
        form = DisciplinaryRecordForm(request.POST)

        if form.is_valid():
            disciplinary_record = form.save(commit=False)
            disciplinary_record.student = student
            disciplinary_record.staff = request.user
            disciplinary_record.save()

            if next_page:
                return redirect(next_page)
            return redirect("Student:profile", id=student.id)

    context = {
        "form": form,
        "current_url": current_url,
        "student": student,
    }

    return render(request, "student/disciplin_form.html", context)


@login_required
def update_disciplinary_record(request, id):
    current_url = request.build_absolute_uri()
    disciplin = get_object_or_404(DisciplinaryRecord, pk=id)
    form = DisciplinaryRecordForm(instance=disciplin)
    next_page = request.GET.get("next_page")

    if request.method == "POST":
        form = DisciplinaryRecordForm(request.POST, instance=disciplin)

        if form.is_valid():
            disciplinary_record = form.save(commit=False)
            disciplinary_record.staff = request.user
            disciplinary_record.save()

            if next_page:
                return redirect(next_page)
            return redirect("Student:profile", id=disciplinary_record.student.id)

    context = {
        "form": form,
        "current_url": current_url,
        "student": disciplinary_record.student,
    }

    return render(request, "student/disciplin_form.html", context)
