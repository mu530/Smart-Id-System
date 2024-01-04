from django import forms
from crispy_forms.helper import FormHelper

from .models import Library, Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("books_left",)


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ("student", "book")

        widgets = {
            "book": forms.HiddenInput(),
        }
