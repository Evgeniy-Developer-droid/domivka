from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy

from public.models import RealEstate
from public.tools.functions import create_real_estate
from user.models import Profile
from user.token import account_activation_token
from django.core.mail import EmailMessage

from user.forms import LoginForm, SignUpForm, ResetPasswordForm, EmailForm, RealEstateForm, ProfileForm


def sign_out(request):
    logout(request)
    return redirect('sign-in')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(request.POST.get('next', 'dashboard'))
                else:
                    return render(request, 'user/login.html', {'form': form, "title": "Вхід",
                                                                 'error': "Аккаунт відключений"})
            else:
                return render(request, 'user/login.html', {'form': form, "title": "Вхід",
                                                             'error': "Неправильний логін або пароль"})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form, "title": "Вхід"})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            if settings.EMAIL_CONFIRM:
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Посилання для активації надіслано на вашу електронну адресу'
                message = render_to_string('user/emails/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'user/info.html', {"title": "Раєстрація",
                    'content': 'Підтвердьте свою електронну адресу, щоб завершити реєстрацію'})
            else:
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form, "title": "Раєстрація"})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'user/info.html',
                      {'title': "Інформація", 'content': 'Дякуємо за підтвердження електронною поштою. Тепер ви можете увійти в обліковий запис.'})
    else:
        return render(request, 'user/info.html',
                      {'title': "Інформація", 'content': 'Посилання для активації недійсне!'})


@login_required(login_url=reverse_lazy('sign-in'))
def dashboard(request):
    estates = RealEstate.objects.filter(user=request.user)
    return render(request, 'user/dashboard.html', {'title': "Моя сторінка", 'items': estates})


@login_required(login_url=reverse_lazy('sign-in'))
def settings_(request):
    try:
        instance = Profile.objects.get(user=request.user)
        form_profile = ProfileForm(request.POST or None, instance=instance)
        if request.method == 'POST':
            if request.POST.get('action', "") == "profile":
                if form_profile.is_valid():
                    form_profile.save()
                    return render(request, 'user/settings.html', {'title': "Налаштування",
                                                                  'form_profile': form_profile,
                                                                  'message': "Номер телефону оновлено"})
        return render(request, 'user/settings.html', {'title': "Налаштування", 'form_profile': form_profile})
    except Profile.DoesNotExist:
        return render(request, 'user/info.html',
                      {'title': "Помилка", 'content': 'Налаштування не знайдено'})


@login_required(login_url=reverse_lazy('sign-in'))
def delete_real_estate(request, pk):
    try:
        instance = RealEstate.objects.get(pk=pk, user=request.user)
        instance.delete()
        return redirect('dashboard')
    except RealEstate.DoesNotExist:
        return render(request, 'user/info.html',
                      {'title': "Помилка", 'content': 'Нерухомість не знайдено або Ви не власник'})


@login_required(login_url=reverse_lazy('sign-in'))
def update_real_estate(request, pk):
    try:
        instance = RealEstate.objects.get(pk=pk, user=request.user)
        form = RealEstateForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.refresh_from_db()
            if 'thumbnail' in request.FILES:
                instance.thumbnail = request.FILES['thumbnail']
                instance.save()
            return redirect('dashboard')
        return render(request, 'user/edit.html', {'title': "Оновлення", 'form': form})
    except RealEstate.DoesNotExist:
        return render(request, 'user/info.html',
                      {'title': "Помилка", 'content': 'Нерухомість не знайдено або Ви не власник'})


@login_required(login_url=reverse_lazy('sign-in'))
def new_real_estate(request):
    if request.method == 'POST':
        form = RealEstateForm(request.POST)
        result = create_real_estate(request, form)
        if result['type'] == 'success':
            return redirect('dashboard')
        return render(request, 'user/new.html', {'title': "Нова нерухомість", 'error': result['message'], 'form': form})
    form = RealEstateForm()
    return render(request, 'user/new.html', {'title': "Нова нерухомість", 'form': form})


def password_reset(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            if settings.EMAIL_CONFIRM:
                current_site = get_current_site(request)
                mail_subject = 'Посилання для активації надіслано на вашу електронну адресу'
                try:
                    user = User.objects.get(email=form.cleaned_data.get('email'))
                    message = render_to_string('user/emails/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return redirect('password-reset-done')
                except User.DoesNotExist:
                    form = EmailForm()
                    return render(request, 'user/password_reset_form.html',
                                  {"title": "Помилка", 'form': form,
                                   'error': 'Користувача з цією електронною поштою не знайдено!'})
    form = EmailForm()
    return render(request, 'user/password_reset_form.html', {"title": "Змінити пароль", 'form': form})


def password_reset_done(request):
    return render(request, 'user/password_reset_done.html', {"title": "Готово"})


def password_reset_complete(request):
    return render(request, 'user/password_reset_complete.html', {"title": "Готово"})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        error = ""
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                pass1 = form.cleaned_data.get('password1', "")
                pass2 = form.cleaned_data.get('password2', "")
                if pass1 == pass2:
                    logout(request)
                    user.set_password(pass1)
                    user.save()
                    return redirect('password-reset-complete')
                else:
                    error = "Пароль не той"
        form = ResetPasswordForm()
        return render(request, 'user/password_reset_confirm.html', {
                                                                    'form': form,
                                                                    'error': error,
                                                                    'validlink': True,
                                                                    "title": "Підтвердьте"})
    else:
        return render(request, 'user/password_reset_confirm.html', {"title": "Підтвердьте"})
