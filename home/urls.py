from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('priceList/', views.PriceList.as_view(), name='price_list'),
    path('practice/', views.PracticeView.as_view(), name='practice'),
    path('choose-video/', views.choose_video_or_paste_url, name='choose_video_or_paste_url'),
]
