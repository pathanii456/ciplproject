from django.contrib import admin
from product.models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "price",
        "discount",
        "image",
        "ssn",
        "is_active",
        "created_on",
        "updated_on",
    ]
    search_fields = ["title", "is_active"]
    ordering = ["title", "id", "price", "discount"]
    filter_horizontal = []
