from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from staffs.decorators import role_required
from .models import Library, Book
from .forms import BookForm, LibraryForm
from .filters import BorrowerFilter, BookFilter


def paginate(request, data, per_page=10):
    paginator = Paginator(data, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
@role_required(["LIBRARIAN"])
def add_book(request):
    form = BookForm()

    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Book Successufully added")
            return redirect("Library:home")

    context = {"form": form}

    return render(request, "library/book_register.html", context)


@login_required
@role_required(["LIBRARIAN"])
def update_book(request, id):
    book = get_object_or_404(Book, pk=id)
    form = BookForm(instance=book)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            messages.success(request, "Book Successufully updated")
            return redirect("Library:home")

    context = {"form": form}

    return render(request, "library/book_register.html", context)


class ReturnBookView(DeleteView):
    model = Library
    success_url = reverse_lazy("Library:home")
    template_name = "library/book_register.html"


@login_required
@role_required(["LIBRARIAN"])
def home(request):
    if request.method == "POST":
        if "book_return" in request.POST:
            id = request.POST.get("id")
            rent = get_object_or_404(Library, pk=id)

            rent.delete()
            messages.success(request, "Book Successufully returned")

        if "book_rent" in request.POST:
            rent_form = LibraryForm(request.POST)

            if rent_form.is_valid():
                rent_form.save()
                messages.success(request, "Successufully rented")

            else:
                rent_errors = rent_form.errors
                messages.error(request, rent_errors)

    books = Book.objects.all()
    borrowers = Library.objects.all()

    book_filter = BookFilter(request.GET, queryset=books)
    books = book_filter.qs

    borrower_filter = BorrowerFilter(request.GET, queryset=borrowers)
    borrowers = borrower_filter.qs

    books = paginate(request, books, 5)
    borrowers = paginate(request, borrowers, 5)

    rent_form = LibraryForm()

    context = {
        "books": books,
        "borrowers": borrowers,
        "borrower_filter": borrower_filter,
        "book_filter": book_filter,
        "rent_form": rent_form,
    }

    return render(request, "library/home.html", context)
