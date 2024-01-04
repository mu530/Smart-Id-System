from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from staffs.decorators import role_required
from addresses.forms import AddressForm

from .forms import CampusForm, DepartmentForm
from .models import Campus, Department
from .filters import CampusFilter, DepartmentFilter


def paginate(request, data, per_page=5):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
@role_required(["REGISTRAR"])
def campus_form(request):
    campus_form = CampusForm()
    address_form = AddressForm()
    department_form = DepartmentForm()

    if request.method == "POST":
        if "campus_submit" in request.POST:
            campus_form = CampusForm(request.POST or None)
            address_form = AddressForm(request.POST)
            if campus_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                campus = campus_form.save(commit=False)
                campus.address = address
                campus.save()
                messages.success(request, f"{ campus.name } campus is Added")
                return redirect(request.path_info)

        if "department_submit" in request.POST:
            department_form = DepartmentForm(request.POST or None)
            if department_form.is_valid():
                department = department_form.save()
                messages.success(request, f"{ department.name } department is Added")
                return redirect(request.path_info)

    context = {
        "department_form": department_form,
        "campus_form": campus_form,
        "address_form": address_form,
        "current_url": request.build_absolute_uri(),
    }

    return render(request, "campus/register.html", context)


@login_required
@role_required(["REGISTRAR"])
def campus_list(request):
    campuses = Campus.objects.all()
    departments = Department.objects.all()

    campus_filter = CampusFilter(request.GET, queryset=campuses)
    campuses = campus_filter.qs

    department_filter = DepartmentFilter(request.GET, queryset=departments)
    departments = department_filter.qs

    campuses = paginate(request, campuses)
    departments = paginate(request, departments)

    context = {
        "departments": departments,
        "campuses": campuses,
        "campus_filter": campus_filter,
        "department_filter": department_filter,
    }

    return render(request, "campus/list.html", context)
