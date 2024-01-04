from django.urls import path
from .views import add_book, home, ReturnBookView, update_book

app_name = "Library"

urlpatterns = [
    path("books/register", add_book, name="register_book"),
    path("books/return", ReturnBookView.as_view(), name="return_book"),
    path("books/<int:id>/update", update_book, name="update_book"),
    path("", home, name="home"),
]
