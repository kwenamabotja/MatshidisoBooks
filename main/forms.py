from django import forms


class ContactForm(forms.Form):
    """To get contact information."""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    # message = forms.
