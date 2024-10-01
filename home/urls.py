from django.urls import path
from .views import HomePageView, PriceList, PracticeView, ChooseVideoView

app_name = 'home'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('priceList/', PriceList.as_view(), name='price_list'),
    path('practice/', PracticeView.as_view(), name='practice'),
    path('choose_video/', ChooseVideoView.as_view(), name='choose_video'),
]
