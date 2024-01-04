from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

from students.models import Student
from campuses.models import Campus


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    total_number = models.PositiveIntegerField()
    books_left = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse("Library:update_book", kwargs={"id": self.pk})

    def clean(self):
        super().clean()

        if self.pk:
            old_books_left = Book.objects.get(pk=self.pk).books_left

            if self.total_number < old_books_left:
                raise ValidationError(
                    "You are removing books that are not on the shelf. Please change the number correctly."
                )

            if self.books_left > self.total_number:
                raise ValidationError(
                    "The number of books left cannot be more than the total number of books."
                )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.books_left = self.total_number

        if self.pk:
            old_books_left = Book.objects.get(pk=self.pk).books_left
            old_total_number = Book.objects.get(pk=self.pk).total_number

            new_number = self.total_number - old_total_number

            if self.total_number >= old_books_left:
                self.books_left += new_number

        super().save(*args, **kwargs)


class Library(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.PROTECT,
        error_messages={
            "unique": "The student did not return a book. ከዚቀደም የተዋሰውን መጽሐፍ አልመለሰም።",
        },
        related_name="rent_book",
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_of_rental = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Libraries"

    def clean(self):
        super().clean()
        if self.book.books_left < 0:
            raise ValidationError("This book is not available.")
