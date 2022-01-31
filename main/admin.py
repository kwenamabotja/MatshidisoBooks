from django.contrib import admin

# Register your models here.
from main.models import Book, Contact


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Custom admin class for book model."""


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Custom admin class for book model."""
