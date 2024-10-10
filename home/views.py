from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


class PriceList(ListView):
    # Define your PriceList view here
    template_name = 'price_list.html'
    # Add any necessary model and context data


class PracticeView(TemplateView):
    template_name = 'practice.html'

class ChooseVideoView(TemplateView):
    template_name = 'choose_video_or_paste_url.html'

def choose_video_or_paste_url(request):
    return render(request, 'choose_video_or_paste_url.html')
