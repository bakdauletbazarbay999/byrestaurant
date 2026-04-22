from django import forms
from .models import Reservation, Order, OrderItem, Dish
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Reservation
        fields = ['full_name', 'phone', 'date', 'time', 'guests', 'table']

class AddToCartForm(forms.Form):
    dish_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone']








from django import forms

class ChatQueryForm(forms.Form):

    message = forms.CharField(
        label='',
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Сұрағыңызды жазыңыз...',
            'autocomplete': 'off',
            'autofocus': 'autofocus'
        })
    )