from django.contrib import admin
from .models import Shop, Product, Customer, Sale, Expense

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "phone")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "selling_price", "stock_quantity")
    list_filter = ("shop",)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "phone")

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("bill_number", "shop", "product", "quantity", "total_amount", "sale_date")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "shop", "amount", "expense_date")
