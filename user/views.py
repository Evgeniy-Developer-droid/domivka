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
from user.token import account_activation_token
from django.core.mail import EmailMessage

from user.forms import LoginForm, SignUpForm, ResetPasswordForm, EmailForm


def sign_out(request):
    logout(request)
    return redirect('sign-in')


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            print("error", form.errors)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'user/login.html', {'form': form, "title": "Login",
                                                                 'error': "Disabled account"})
            else:
                return render(request, 'user/login.html', {'form': form, "title": "Login",
                                                             'error': "Invalid login or password"})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form, "title": "Login"})


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
                mail_subject = 'Activation link has been sent to your email id'
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
                return render(request, 'user/info.html', {
                    'content': 'Please confirm your email address to complete the registration'})
            else:
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form, "title": "Register"})


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
                      {'content': 'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request, 'user/info.html',
                      {'content': 'Activation link is invalid!'})


@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html', {})


def password_reset(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            if settings.EMAIL_CONFIRM:
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'
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
                                  {"title": "Change password", 'form': form,
                                   'error': 'User with this email not found!'})
    form = EmailForm()
    return render(request, 'user/password_reset_form.html', {"title": "Change password", 'form': form})


def password_reset_done(request):
    return render(request, 'user/password_reset_done.html', {"title": "Done"})


def password_reset_complete(request):
    return render(request, 'user/password_reset_complete.html', {"title": "Done"})


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
                    error = "Password not same"
        form = ResetPasswordForm()
        return render(request, 'user/password_reset_confirm.html', {
                                                                    'form': form,
                                                                    'error': error,
                                                                    'validlink': True,
                                                                    "title": "Confirm"})
    else:
        return render(request, 'user/password_reset_confirm.html', {"title": "Confirm"})
