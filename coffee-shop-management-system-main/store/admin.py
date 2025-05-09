from django.contrib import admin
from .models import Product, Order, Profile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('stock',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'ordered_at', 'is_ordered')
    list_filter = ('is_ordered', 'ordered_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username',)
