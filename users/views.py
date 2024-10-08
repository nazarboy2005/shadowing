import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.views import View

from users.forms import (
    EmailVerificationForm,
    LoginForm,
    AccountModelForm,
)
from users.models import ConfirmationCodesModel, AccountModel

UserModel = get_user_model()


def send_confirmation_email(user, code):
    subject = 'Verify your email address'
    message = f'Your confirmation code is {code}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# RegisterView
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

        # Store the registration data temporarily in the session, DO NOT create the user yet
        request.session['temp_registration_data'] = {
            'username': username,
            'email': email,
            'password': password1,
        }

        # Generate a random confirmation code (6 digits)
        confirmation_code = str(random.randint(100000, 999999))

        # Send confirmation email
        temp_user = User(username=username, email=email, password=password1)  # User not saved yet
        success = send_confirmation_email(temp_user, confirmation_code)

        if success:
            # Save the confirmation code in session for verification
            request.session['confirmation_code'] = confirmation_code
            messages.success(request, 'Please verify your email to complete the registration process.')
            return redirect('users:verify_email')
        else:
            messages.error(request, 'Failed to send confirmation email. Please try again later.')
            return redirect('users:register')


def verify_email(request):
    email = request.session.get('temp_registration_data', {}).get('email')
    if not email:
        messages.error(request, 'Email not found. Please register again.')
        return redirect('users:register')

    if request.method == 'GET':
        form = EmailVerificationForm()
        return render(request, 'verify-email.html', {'form': form, 'email': email})

    elif request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            received_code = form.cleaned_data['code']
            saved_code = request.session.get('confirmation_code')

            if received_code == saved_code:
                # Proceed to save the user as the email is now verified
                user_data = request.session.get('temp_registration_data')
                if user_data:
                    # Create user
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password']
                    )
                    user.is_active = True  # Activate the user
                    user.save()

                    # Now create the AccountModel entry linked to this user
                    AccountModel.objects.create(user=user)

                    # Clear session data after registration
                    del request.session['temp_registration_data']
                    del request.session['confirmation_code']

                    messages.success(request, 'Email verified successfully! Please log in.')
                    return redirect('users:login')
                else:
                    messages.error(request, 'Registration data not found.')
                    return redirect('users:register')
            else:
                messages.error(request, 'Invalid confirmation code.')

        return render(request, 'verify-email.html', {'form': form, 'email': email})




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

