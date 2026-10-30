from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Shop, Product, Customer, Expense, Sale

class RegisterForm(UserCreationForm):
    shop_name = forms.CharField(max_length=150, label="Shop / business name")
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "shop_name", "password1", "password2")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "sku", "purchase_price", "selling_price", "stock_quantity", "low_stock_limit")
        widgets = {
            "purchase_price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "selling_price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "stock_quantity": forms.NumberInput(attrs={"step": "0.001", "min": "0"}),
            "low_stock_limit": forms.NumberInput(attrs={"step": "0.001", "min": "0"}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "phone", "address")

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("title", "amount", "expense_date", "notes")
        widgets = {"expense_date": forms.DateInput(attrs={"type": "date"})}

class SaleForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.none(), required=False)
    product = forms.ModelChoiceField(queryset=Product.objects.none())
    quantity = forms.DecimalField(min_value=0.001, max_digits=12, decimal_places=3)
    paid_amount = forms.DecimalField(min_value=0, max_digits=12, decimal_places=2, initial=0)

    def __init__(self, *args, shop=None, **kwargs):
        super().__init__(*args, **kwargs)
        if shop:
            self.fields["customer"].queryset = Customer.objects.filter(shop=shop)
            self.fields["product"].queryset = Product.objects.filter(shop=shop, stock_quantity__gt=0)
