from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'base.html')


def error404(request, exception):
    return render(request, '404.html')
