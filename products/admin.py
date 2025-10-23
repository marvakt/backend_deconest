from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'room', 'stock', 'is_archived', 'created_at')
    list_filter = ('room', 'is_archived', 'created_at')
    search_fields = ('title', 'room')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock', 'is_archived')
