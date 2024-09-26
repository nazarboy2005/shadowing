import random
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView

from users.forms import RegisterForm, EmailVerificationForm, LoginForm, AccountModelForm
from users.models import ConfirmationCodesModel, AccountModel

UserModel = get_user_model()


def send_confirmation_email(user):
    random_code = random.randint(100000, 999999)
    active_code = ConfirmationCodesModel.objects.filter(code=random_code).exists()
    if active_code:
        send_confirmation_email(user)
    else:
        ConfirmationCodesModel.objects.create(
            code=random_code,
            user=user
        )
        try:
            send_mail(message=str(random_code), subject='Confirmation Code', recipient_list=[user.email],
                      from_email=settings.EMAIL_HOST_USER)
            return True

        except ConnectionError as e:
            return False


def verify_email(request):
    if request.method == 'GET':
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'verify-email.html')
    else:
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            received_code = form.cleaned_data["code"]
            user_and_code = ConfirmationCodesModel.objects.filter(code=received_code).first()
            if user_and_code:
                time_now = datetime.now(pytz.timezone(settings.TIME_ZONE))
                sent_time = user_and_code.created_at.astimezone(pytz.timezone(settings.TIME_ZONE)) + timedelta(
                    minutes=2)
                if sent_time > time_now:
                    db_user = UserModel.objects.filter(id=user_and_code.user.id).first()
                    db_user.is_active = True
                    db_user.save()
                    user_and_code.delete()
                    return redirect('users:login')

                else:
                    messages.error(request, 'Confirmation Code is expired')
            else:
                messages.error(request, 'The Code Is Invalid')

        else:
            messages.error(request, 'Wrong Password')
        return redirect('users:verify_email')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        if send_confirmation_email(user):
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'The email could not be sent! Please Try again Later!')
            return redirect(self.success_url)

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(request=self.request, message=form.errors)
        return redirect('users:register')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        next_page = self.request.POST.get('next', '/')
        if 'comment' in next_page:
            next_page = next_page.replace('comment', 'details')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user=user)
            print(f"Redirecting to: {next_page}")
            return redirect(next_page)
        else:
            storage = messages.get_messages(self.request)
            storage.used = True
            messages.error(self.request, 'Wrong Password or Username')

            return redirect('users:login')

    def form_invalid(self, form):
        storage = messages.get_messages(self.request)
        storage.used = True
        messages.error(self.request, 'Wrong Password or Username')
        return redirect('users:login')


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('pages:home')


class ProfileView(UpdateView): #LoginRequiredMixin
    template_name = 'profile.html'
    form_class = AccountModelForm
    success_url = reverse_lazy('users:profile')
    context_object_name = 'profile'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        account, _ = AccountModel.objects.get_or_create(user=self.request.user)
        return account


class BillingsView(TemplateView):
    template_name = 'billings.html'



class FlashCardsView(TemplateView):
    template_name = 'flashcard.html'

class WordsView(TemplateView):
    template_name = 'words.html'