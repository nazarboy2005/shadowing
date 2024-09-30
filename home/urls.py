from django.urls import path
from home.views import HomePageView, PriceList, PracticeView
from . import views

app_name = 'home'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('priceList/', PriceList.as_view(), name='price_list'),
    path('practice/', PracticeView.as_view(), name='practice'),
    path('login/', views.login_view, name='login'),




]
