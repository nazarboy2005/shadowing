
from django.urls import path

from users.views import RegisterView, LoginView, ProfileView, logout_view, verify_email, BillingsView, FlashCardsView, WordsView

app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', verify_email, name='verify_email'),
    path('billings/', BillingsView.as_view(), name='billings'),
    path('flashcard/', FlashCardsView.as_view(), name='flashcards'),
    path('words/', WordsView.as_view(), name='words'),
]