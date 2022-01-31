from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    """To get contact information."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    # mobile_number = forms.RegexField(
    #     regex=r'^\+?1?\d{9,15}$',
    #     error_message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    # )
    # message = forms.


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )


class OrderBookForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.'
    )
    # book-id, mobile number, address, banking details
