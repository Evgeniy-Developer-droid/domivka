from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from public.models import RealEstate
from user.models import Profile


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Repeat Password'}))


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email', 'autocomplete': 'off'}))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class RealEstateForm(forms.ModelForm):
    CITY = (('', 'City'),)
    Region = (('', 'Region'),)
    city = forms.CharField(widget=forms.HiddenInput())
    city_code = forms.CharField(widget=forms.Select(attrs={'id': 'city'}, choices=CITY))
    region = forms.CharField(widget=forms.HiddenInput())
    region_code = forms.CharField(widget=forms.Select(attrs={'id': 'region'}, choices=Region))

    class Meta:
        model = RealEstate
        fields = ('thumbnail', 'description', 'price', 'rooms', 'address',
                  'city', 'region', 'city_code', 'region_code', 'type_real_estate', 'service_type', )

    def __init__(self, *args, **kwargs):
        super(RealEstateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "+380000000000"
    }))
    action = forms.CharField(widget=forms.HiddenInput(attrs={
        "value":"profile"
    }))

    class Meta:
        model = Profile
        fields = ('phone', )
