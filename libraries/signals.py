from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import Library


@receiver(pre_save, sender=Library)
def update_books_left(sender, instance, **kwargs):
    if (
        instance.pk is None
    ):  # Only update books_left when creating a new Library instance
        instance.book.books_left -= 1
        instance.book.save()

    if instance.pk:
        old_instance = Library.objects.get(pk=instance.pk)
        old_book = old_instance.book
        new_book = instance.book

        if old_book != new_book:
            old_book.books_left += 1
            new_book.books_left -= 1

            old_book.save()
            new_book.save()


@receiver(pre_delete, sender=Library)
def restore_books_left(sender, instance, **kwargs):
    instance.book.books_left += 1
    instance.book.save()
