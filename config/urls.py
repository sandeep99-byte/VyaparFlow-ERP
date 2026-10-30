from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),
    path("customers/", views.customers, name="customers"),
    path("customers/add/", views.add_customer, name="add_customer"),
    path("expenses/", views.expenses, name="expenses"),
    path("expenses/add/", views.add_expense, name="add_expense"),
    path("sales/", views.sales, name="sales"),
    path("sales/new/", views.new_sale, name="new_sale"),
    path("sales/<int:sale_id>/", views.sale_detail, name="sale_detail"),
]
