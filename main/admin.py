from django.contrib import admin

# Register your models here.
from main.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Custom admin class for book model."""
