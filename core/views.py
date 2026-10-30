from decimal import Decimal
from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, F
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, ProductForm, CustomerForm, ExpenseForm, SaleForm
from .models import Shop, Product, Customer, Sale, Expense

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")

def get_shop(user):
    return Shop.objects.filter(owner=user).first()

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Shop.objects.create(owner=user, name=form.cleaned_data["shop_name"])
            login(request, user)
            messages.success(request, "Account and shop created. Welcome!")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    shop = get_shop(request.user)
    if not shop:
        messages.error(request, "Your shop profile is missing. Please register again or contact the administrator.")
        return redirect("logout")
    today = timezone.localdate()
    sales_today = Sale.objects.filter(shop=shop, sale_date__date=today).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")
    expenses_today = Expense.objects.filter(shop=shop, expense_date=today).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    all_sales = Sale.objects.filter(shop=shop).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")
    all_expenses = Expense.objects.filter(shop=shop).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    context = {
        "shop": shop,
        "product_count": Product.objects.filter(shop=shop).count(),
        "customer_count": Customer.objects.filter(shop=shop).count(),
        "sales_today": sales_today,
        "expenses_today": expenses_today,
        "estimated_profit": all_sales - all_expenses,
        "low_stock": Product.objects.filter(shop=shop, stock_quantity__lte=F("low_stock_limit")).order_by("stock_quantity")[:5],
        "recent_sales": Sale.objects.filter(shop=shop).select_related("product", "customer")[:5],
    }
    return render(request, "dashboard.html", context)

@login_required
def products(request):
    shop = get_shop(request.user)
    return render(request, "products/list.html", {"shop": shop, "products": Product.objects.filter(shop=shop)})

@login_required
def add_product(request):
    shop = get_shop(request.user)
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.shop = shop
        obj.save()
        messages.success(request, "Product added.")
        return redirect("products")
    return render(request, "form.html", {"form": form, "title": "Add product", "back_url": "products"})

@login_required
def customers(request):
    shop = get_shop(request.user)
    return render(request, "customers/list.html", {"customers": Customer.objects.filter(shop=shop)})

@login_required
def add_customer(request):
    shop = get_shop(request.user)
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.shop = shop
        obj.save()
        messages.success(request, "Customer added.")
        return redirect("customers")
    return render(request, "form.html", {"form": form, "title": "Add customer", "back_url": "customers"})

@login_required
def expenses(request):
    shop = get_shop(request.user)
    return render(request, "expenses/list.html", {"expenses": Expense.objects.filter(shop=shop)})

@login_required
def add_expense(request):
    shop = get_shop(request.user)
    form = ExpenseForm(request.POST or None, initial={"expense_date": date.today()})
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.shop = shop
        obj.save()
        messages.success(request, "Expense recorded.")
        return redirect("expenses")
    return render(request, "form.html", {"form": form, "title": "Add expense", "back_url": "expenses"})

@login_required
def sales(request):
    shop = get_shop(request.user)
    return render(request, "sales/list.html", {"sales": Sale.objects.filter(shop=shop).select_related("product", "customer")})

@login_required
def new_sale(request):
    shop = get_shop(request.user)
    form = SaleForm(request.POST or None, shop=shop)
    if request.method == "POST" and form.is_valid():
        product = form.cleaned_data["product"]
        quantity = form.cleaned_data["quantity"]
        paid = form.cleaned_data["paid_amount"]
        customer = form.cleaned_data["customer"]
        if product.shop_id != shop.id or (customer and customer.shop_id != shop.id):
            return HttpResponseForbidden("Invalid product or customer.")
        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product.pk, shop=shop)
            if product.stock_quantity < quantity:
                form.add_error("quantity", f"Only {product.stock_quantity} available in stock.")
            else:
                total = (product.selling_price * quantity).quantize(Decimal("0.01"))
                if paid > total:
                    form.add_error("paid_amount", "Paid amount cannot be greater than the bill total.")
                else:
                    last = Sale.objects.filter(shop=shop).count() + 1
                    sale = Sale.objects.create(
                        shop=shop, customer=customer, product=product,
                        bill_number=f"VF-{timezone.localdate():%Y%m%d}-{last:04d}",
                        quantity=quantity, unit_price=product.selling_price,
                        total_amount=total, paid_amount=paid
                    )
                    product.stock_quantity -= quantity
                    product.save(update_fields=["stock_quantity"])
                    messages.success(request, f"Bill {sale.bill_number} created.")
                    return redirect("sale_detail", sale_id=sale.id)
    return render(request, "sales/new.html", {"form": form})

@login_required
def sale_detail(request, sale_id):
    shop = get_shop(request.user)
    sale = get_object_or_404(Sale.objects.select_related("product", "customer", "shop"), pk=sale_id, shop=shop)
    return render(request, "sales/detail.html", {"sale": sale})
