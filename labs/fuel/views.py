from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from echrono.models import FuelPods,FuelTransactions,Airplane,User


def index(request):
    for pod in FuelPods.objects.all():
        pod.fill_percentage = round((pod.fill_level/pod.capacity) * 100,2)
        pod.save()
    return render(request, 'fuel/index.html', {'fuelpods':FuelPods.objects.all()})

def pod(request,id):
    print(FuelTransactions.objects.filter(id=id).all())
    pod = FuelPods.objects.filter(id=id).first()
    if request.method == 'POST':
        if 'refuel' in request.POST:
            if pod.fill_level - float(request.POST.get('quantity')) >= 0:
                pod.fill_level = pod.fill_level - float(request.POST.get('quantity'))
                pod.fill_percentage = round((pod.fill_level / pod.capacity) * 100, 2)
                FuelTransactions(buyer=User.objects.filter(id=request.POST.get('user')).first(),
                                 quantity=float(request.POST.get('quantity')),
                                 aircraft_id=Airplane.objects.filter(id=request.POST.get('airplane')).first(),
                                 fuel_pod=pod,
                                 date=datetime.now()
                                 ).save()
                pod.save()

        if 'refill' in request.POST:
            if pod.fill_level + float(request.POST.get('quantity')) <= pod.capacity:
                pod.fill_level = pod.fill_level + float(request.POST.get('quantity'))
                pod.fill_percentage = round((pod.fill_level / pod.capacity) * 100,2)
                pod.save()
    return render(request, 'fuel/pod.html', {'pod': pod,
                                             'transactions': FuelTransactions.objects.filter(fuel_pod=pod).all(),
                                             'airplanes': Airplane.objects.all(),
                                             'users': User.objects.all()}
                  )