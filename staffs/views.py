from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.core.paginator import Paginator

from .forms import StaffRegistrationForm, StaffChangeForm
from .filters import StaffFilter

Staff = get_user_model()


def paginate(request, data, per_page=5):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def about(request):
    return render(request, "base/about.html")


@login_required
def staff_register(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not allowed")

    form = StaffRegistrationForm()

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, (f"Account created for {user.username}"))
            return redirect("Staff:staff_detail", user.id)
        else:
            messages.error(request, ("please fix the errors"))

    context = {"form": form}

    return render(request, "staff/staff_register.html", context)


@login_required
def staff_update(request, user_id):
    staff = get_object_or_404(Staff, pk=user_id)

    if (not request.user.is_superuser) and (request.user != staff):
        return HttpResponse("You are not allowed")

    form = StaffChangeForm(instance=staff)

    if request.method == "POST":
        form = StaffChangeForm(request.POST, request.FILES, instance=staff)

        if form.is_valid():
            user = form.save()
            messages.success(request, (f"Profile updated for {user.username}"))
            return redirect("Staff:staff_detail", user.id)
        else:
            messages.error(request, ("please fix the errors"))

    context = {"form": form, "staff": staff}

    return render(request, "staff/update_profile.html", context)


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "staff/change_password.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
def staff_list_view(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not allowed")

    staffs = Staff.objects.all()
    if request.method == "GET":
        sort_by = request.GET.get("sort_by", "")
        if sort_by in ("username", "role"):
            staffs = staffs.order_by(sort_by)
    staff_filter = StaffFilter(request.GET, queryset=staffs)
    staffs = staff_filter.qs

    staffs = paginate(request, staffs)
    context = {
        "staffs": staffs,
        "staff_filter": staff_filter,
    }

    return render(request, "staff/staff_list.html", context)


@login_required
def staff_detail_view(request, user_id):
    staff = get_object_or_404(Staff, pk=user_id)

    if (not request.user.is_superuser) and (request.user != staff):
        return HttpResponse("You are not allowed")

    context = {"staff": staff}

    return render(request, "staff/staff_detail.html", context)


def staff_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next = request.GET.get("next", "Staff:staff_list")

            return redirect(next)

        else:
            messages.error(request, "user not found.")

    return render(request, "staff/login.html")


def staff_logout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.error(request, ("you are not even logged in"))

        return redirect("/")

    return redirect("/")


class ResetPasswordView(PasswordResetView):
    template_name = "staff/password_reset.html"
    email_template_name = "staff/email/password_reset_email.html"
    subject_template_name = "staff/email/password_reset_subject.txt"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("Staff:password_reset_done")
    from_email = "studid@uog.com"


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = "staff/password_reset_done.html"


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "staff/password_reset_confirm.html"
    success_url = reverse_lazy("Staff:password_reset_complete")


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = "staff/password_reset_complete.html"


def index(request):
    context = {
        "title": "Welcome to University of Gondar!",
        "subtitle": "Learn more about our services",
        "services": [
            {
                "title": "Undergraduate Programs",
                "description": "We offer a wide range of undergraduate programs in various fields of study, including: Accounting, Agriculture, Architecture, Business Administration, Civil Engineering, Computer Science, Education, Environmental Science, Law, Medicine, Nursing, Pharmacy, Public Health, and more.",
            },
            {
                "title": "Graduate Programs",
                "description": "We offer several graduate programs, including master's and doctoral degrees in various fields of study, including: Accounting, Agriculture, Architecture, Business Administration, Civil Engineering, Computer Science, Education, Environmental Science, Law, Medicine, Nursing, Pharmacy, Public Health, and more.",
            },
            {
                "title": "Research",
                "description": "We conduct research in various areas, including health, agriculture, technology, social sciences, and humanities.",
            },
            {
                "title": "Community Engagement",
                "description": "We work closely with local communities to address social and economic challenges, including health, education, and poverty reduction.",
            },
            {
                "title": "Continuing Education",
                "description": "We offer continuing education programs and professional development courses for working professionals and lifelong learners.",
            },
            {
                "title": "International Programs",
                "description": "We offer international programs and exchange opportunities for students and faculty to study and collaborate with partner institutions around the world.",
            },
        ],
        "contact": {
            "email": "info@example.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Main St, Anytown USA",
        },
        "university": {
            "name": "University of Gondar",
            "location": "Gondar, Ethiopia",
            "description": "The University of Gondar is a public research university located in the historic city of Gondar in Ethiopia. It was established in 1954 and has since grown into one of the largest and most prestigious universities in the country.",
            "photo": "https://example.com/university-of-gondar.jpg",
        },
    }
    return render(request, "staff/index.html", context)
