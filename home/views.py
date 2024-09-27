from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


class PriceList(TemplateView):
    template_name = 'price_list.html'



class PracticeView(TemplateView):
    template_name = 'choose_video_or_paste_url.html'
