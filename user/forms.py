from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, validate_slug

from public.models import RealEstate
from user.models import Profile

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Нікнейм не повинен містити кирилицю')

# def unic(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Повторіть пароль'}))


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Електронна пошта', 'autocomplete': 'off'}))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FirstLastNameForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Ім'я"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Прізвище"
    }))
    action = forms.CharField(widget=forms.HiddenInput(attrs={
        "value": "first_last_name"
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    # def __init__(self, *args, **kwargs):
    #     super(FirstLastNameForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


class SignUpForm(forms.ModelForm):
    validate_slug.message = "Введіть дійсний «Нікнейм», що складається з латинських літер, цифр, символів підкреслення або дефісів."
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Ім'я"
    }))
    username = forms.CharField(max_length=30, validators=[validate_slug], widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Нікнейм"
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Прізвище"
    }))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Пароль'}), validators=[validate_password])
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Повторіть пароль'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Електронна пошта', 'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2', )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Користувач з такою електронною поштою існує")
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Користувач з таким нікнеймом існує")
        if password != password2:
            self.add_error('password', "Паролі не співпадають")


class RealEstateForm(forms.ModelForm):
    CITY = (('', 'Місто'),)
    Region = (('', 'Область'),)
    city = forms.CharField(widget=forms.HiddenInput())
    city_code = forms.CharField(widget=forms.Select(attrs={'id': 'city'}, choices=CITY))
    region = forms.CharField(widget=forms.HiddenInput())
    region_code = forms.CharField(widget=forms.Select(attrs={'id': 'region'}, choices=Region))

    class Meta:
        model = RealEstate
        fields = ('thumbnail', 'description', 'price', 'rooms', 'address', 'name',
                  'city', 'region', 'city_code', 'region_code', 'type_real_estate', 'service_type', )

    def __init__(self, *args, **kwargs):
        super(RealEstateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "380000000000"
    }), required=False)
    facebook = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "facebook.com..."
    }), required=False)
    linkedin = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "linkedin.com..."
    }), required=False)
    youtube = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "youtube.com..."
    }), required=False)
    instagram = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "instagram.com..."
    }), required=False)
    skype = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "yourskypename"
    }), required=False)
    whatsapp = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "380000000000"
    }), required=False)
    viber = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "380000000000"
    }), required=False)
    telegram = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "yourtelegramname"
    }), required=False)
    action = forms.CharField(widget=forms.HiddenInput(attrs={
        "value": "profile"
    }))

    class Meta:
        model = Profile
        fields = ('phone', 'facebook', 'linkedin', 'youtube', 'instagram',
                  'skype', 'whatsapp', 'viber', 'telegram',)
