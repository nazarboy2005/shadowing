
from django.urls import path

from users.views import RegisterView, LoginView, ProfileView, logout_view, verify_email, PaymentsView, FlashCardsView, WordsView, LearningView

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

]