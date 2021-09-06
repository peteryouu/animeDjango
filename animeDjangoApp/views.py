from django.shortcuts import render

from animeDjangoApp import animefunctions
#our home page view

def home(request):
    return render(request, 'index.html')

def result(request):
    fav_anime = str(request.GET['fav_anime'])

    result = animefunctions.getPredictions(fav_anime)

    return render(request, 'result.html',{'result':result})


