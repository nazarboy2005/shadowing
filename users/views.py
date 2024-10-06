import random
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.views import View

from users.forms import (
    EmailVerificationForm,
    LoginForm,
    AccountModelForm,
)
from users.models import ConfirmationCodesModel, AccountModel

UserModel = get_user_model()


def send_confirmation_email(user):
    max_attempts = 5
    for _ in range(max_attempts):
        random_code = random.randint(100000, 999999)
        if not ConfirmationCodesModel.objects.filter(code=random_code).exists():
            ConfirmationCodesModel.objects.create(code=random_code, user=user)
            try:
                send_mail(
                    subject='Confirmation Code',
                    message=f'Your confirmation code is: {random_code}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return True
            except (ConnectionError, BadHeaderError) as e:
                # Log the error if needed
                return False
    # If all attempts fail
    return False


def verify_email(request):
    if request.method == 'GET':
        form = EmailVerificationForm()
        return render(request, 'verify-email.html', {'form': form})
    else:
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            received_code = form.cleaned_data['code']
            user_code = ConfirmationCodesModel.objects.filter(code=received_code).first()
            if user_code:
                time_now = datetime.now(pytz.timezone(settings.TIME_ZONE))
                code_expiry_time = user_code.created_at + timedelta(minutes=2)
                if code_expiry_time > time_now:
                    user = user_code.user
                    user.is_active = True
                    user.save()
                    user_code.delete()
                    messages.success(request, 'Email verified successfully! Please log in.')
                    return redirect('users:login')
                else:
                    user_code.delete()  # Remove expired code
                    messages.error(request, 'Confirmation code has expired.')
            else:
                messages.error(request, 'Invalid confirmation code.')
        else:
            messages.error(request, 'Please enter a valid confirmation code.')
        return render(request, 'verify-email.html', {'form': form})


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            error_message = "Passwords do not match."
            return render(request, self.template_name, {'error_message': error_message})

        if User.objects.filter(username=username).exists():
            error_message = "Username already exists."
            return render(request, self.template_name, {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = "Email already exists."
            return render(request, self.template_name, {'error_message': error_message})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Create an AccountModel instance for the new user
        AccountModel.objects.create(user=user)

        messages.success(request, 'Your account has been created successfully! Please verify your email.')
        return redirect('users:login')


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            next_page = self.request.GET.get('next') or reverse_lazy('home:home')
            return redirect(next_page)
        else:
            messages.error(self.request, 'Invalid username or password.')
            return redirect('users:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials.')
        return self.render_to_response(self.get_context_data(form=form))

def logout_view(request):
    logout(request)
    return redirect('home:home')

class ProfileView(LoginRequiredMixin, UpdateView):
    """Allow users to update their profile."""
    template_name = 'profile.html'
    form_class = AccountModelForm
    success_url = reverse_lazy('users:profile')
    context_object_name = 'profile'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        # Try to get the AccountModel for the logged-in user
        try:
            return AccountModel.objects.get(user=self.request.user)
        except AccountModel.DoesNotExist:
            # If no AccountModel exists, create one for the user
            return AccountModel.objects.create(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return self.render_to_response(self.get_context_data(form=form))


class PaymentsView(LoginRequiredMixin, TemplateView):
    template_name = 'payment.html'
    login_url = reverse_lazy('users:login')


class FlashCardsView(LoginRequiredMixin, TemplateView):
    template_name = 'flashcard.html'
    login_url = reverse_lazy('users:login')


class WordsView(LoginRequiredMixin, TemplateView):
    template_name = 'words.html'
    login_url = reverse_lazy('users:login')


class LearningView(LoginRequiredMixin, TemplateView):
    template_name = 'learn.html'
    login_url = reverse_lazy('users:login')


class ProfileEditView(UpdateView):
    model = AccountModel
    form_class = AccountModelForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')  # Redirect to profile page after editing

    def get_object(self):
        return AccountModel.objects.get(user=self.request.user)

