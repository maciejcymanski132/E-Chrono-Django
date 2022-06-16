from django.http import HttpResponse
from django.shortcuts import render, redirect

from echrono.models import FuelPods, FuelTransactions, Airplane, User, Glider


def index(request):
    if request.method == "POST":
        print('happens')
        print(request.POST)
        if 'airplane' in request.POST:
            print('airplane/' + request.POST.get('glider'))
            return redirect('airplane/' + request.POST.get('airplane'))

        if 'glider' in request.POST:
            print('glider/' + request.POST.get('glider'))
            return redirect('glider/' + request.POST.get('glider'))

    return render(request, 'review/index.html', {"airplanes": Airplane.objects.all(), "gliders": Glider.objects.all()})


def glider(request):
    return render(request, 'review/glider.html', {"gliders": Glider.objects.all()})


def airplane(request):
    return render(request, 'review/airplane.html', {"airplanes": Airplane.objects.all()})