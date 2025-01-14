from django import forms
from .models import ShippingAddress
from datetime import date

class ShippingForm(forms.ModelForm):
    DIVISION_CHOICES = (
        ('Dhaka', 'Dhaka'),
        ('Chittagong', 'Chittagong'),
        ('Rajshahi', 'Rajshahi'),
        ('Khulna', 'Khulna'),
        ('Barishal', 'Barishal'),
        ('Sylhet', 'Sylhet'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
    )

    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }),
        required=True
    )

    shipping_email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        }),
        required=True
    )

    shipping_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 1'
        }),
        required=True
    )

    shipping_address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Address Line 2'
        }),
        required=False
    )

    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        }),
        required=True
    )

    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Zip Code'
        }),
        required=True
    )

    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Country'
        }),
        required=True
    )

    shipping_division = forms.ChoiceField(
        choices=DIVISION_CHOICES,
        label="",
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=True
    )
    
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_address1',
            'shipping_address2', 'shipping_city', 'shipping_division',
            'shipping_zipcode', 'shipping_country'
        ]
        exclude = ['user'] 
        
        
        



class PaymentForm(forms.Form):
    
    card_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name On Card'})
    )
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'})
    )
    card_exp_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Expiration Date (MM/YY)'})
    )
    card_cvv_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV Code'})
    )
    card_address1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'})
    )
    card_address2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}),
        required=False
    )
    card_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing City'})
    )
    card_division = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Division'})
    )
    card_zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'})
    )
    card_country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Country'})
    )


        
