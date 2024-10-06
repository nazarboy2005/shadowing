from django.urls import path

from users.views import RegisterView, LoginView, ProfileView, logout_view, verify_email, PaymentsView, FlashCardsView, \
    WordsView, LearningView, ProfileEditView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', verify_email, name='verify_email'),
    path('billings/', PaymentsView.as_view(), name='payments'),
    path('flashcard/', FlashCardsView.as_view(), name='flashcards'),
    path('words/', WordsView.as_view(), name='words'),
    path('learn/', LearningView.as_view(), name='learn'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='users/change_password.html'),
         name='change_password'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),

]
