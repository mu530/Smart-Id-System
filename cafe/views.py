import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from staffs.decorators import role_required
from students.models import Student
from .models import MealPeriod, Attendance
from .forms import AttendanceForm, MealForm
from .filters import CafeUserFilter, MealFilter


def paginate(request, data, per_page=10):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
@role_required(["CAFE_STAFF"])
def add_meal(request):
    meal_form = MealForm()

    if request.method == "POST":
        meal_form = MealForm(request.POST)

        if meal_form.is_valid():
            meal = meal_form.save()
            messages.success(request, "ተመዝግቧል። Regitered.")
            return redirect("Cafe:home")

    return render(request, "cafe/add_meal.html", {"meal_form": meal_form})


@login_required
@role_required(["CAFE_STAFF"])
def update_meal(request, meal_id):
    Attendance.create_attendance_for_today()
    meal_period = get_object_or_404(MealPeriod, pk=meal_id)
    meal_form = MealForm(instance=meal_period)

    if request.method == "POST":
        meal_form = MealForm(request.POST, instance=meal_period)

        if meal_form.is_valid():
            meal = meal_form.save()
            messages.success(request, "ተቀይሯል Updated.")
            return redirect("Cafe:home")

    return render(request, "cafe/add_meal.html", {"meal_form": meal_form})


@login_required
@role_required(["CAFE_STAFF"])
def list_meal(request):
    Attendance.create_attendance_for_today()
    meal_periods = MealPeriod.objects.all()

    meal_period_filter = MealFilter(request.POST, queryset=meal_periods)
    meal_periods = meal_period_filter.qs

    meal_periods = paginate(request, meal_periods)

    if request.method == "POST":
        if "delete_period" in request.POST:
            meal_id = request.POST.get("meal_id")
            meal = get_object_or_404(MealPeriod, pk=meal_id)
            meal.delete()
            messages.success(request, "ተሰርዟል Deleted.")

    context = {
        "meal_periods": meal_periods,
        "meal_period_filter": meal_period_filter,
    }

    return render(request, "cafe/list_meal.html", context)


@login_required
@role_required(["CAFE_STAFF"])
def meal_card(request, meal_id):
    Attendance.create_attendance_for_today()
    meal_period = get_object_or_404(MealPeriod, pk=meal_id)

    cafe_users = Attendance.objects.filter(
        meal_period=meal_period, date_checked=datetime.date.today()
    ).order_by("has_eaten")

    if request.method == "POST":
        if "meal_card" in request.POST:
            meal_card_id = int(request.POST.get("meal_card_id"))
            meal_card = get_object_or_404(Attendance, pk=meal_card_id)

            if meal_card.has_eaten:
                messages.error(
                    request,
                    f"{meal_card.student.full_name_am()} ከዚ ቀደም {meal_card.meal_period.meal_period_am} ተመግቧል። {meal_card.student.full_name()} has eaten {meal_card.meal_period.meal_period_am}",
                )
            else:
                meal_card.has_eaten = True
                meal_card.save()
                messages.success(request, "ተመዝግቧል። Regitered.")

    cafe_users_filter = CafeUserFilter(request.POST, queryset=cafe_users)
    cafe_users = cafe_users_filter.qs

    cafe_users = paginate(request, cafe_users)

    context = {
        "meal_period": meal_period,
        "cafe_users": cafe_users,
        "cafe_users_filter": cafe_users_filter,
    }

    return render(request, "cafe/meal_card.html", context)
