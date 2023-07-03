from orders.models import Order
from django import forms

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",  "placeholder": "Введите имя",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",  "placeholder": "Введите фамилию",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",  "placeholder": "Введите адрес эл. почты",
    }))
    adress = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",  "placeholder": "Введите адрес",
    }))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'adress']