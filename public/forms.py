from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "Ім'я"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Електронна пошта'}))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Введіть свій коментар...'}))
