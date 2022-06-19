from django.http import HttpResponse
from django.shortcuts import render, redirect
from .FlightDataValidator import *
import datetime
from .models import *

models_dictionary = {
    'Glider': Glider,
    'Airplane': Airplane,
    'User': User
}


def index(request):
    context = {
        'chrono': Chronometer.objects.all(),
        'airplanes': Airplane.objects.all(),
        'gliders': Glider.objects.all(),
        'users': User.objects.all(),
        'airplane_flights': AirplaneFlight.objects.all()
    }
    return render(request, 'echrono/index.html', context)


def manage(request):
    context = {
        'airplanes': Airplane.objects.all(),
        'gliders': Glider.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'echrono/manage.html', context)


def add_flight(request):
    request_validation_response = FlightDataValidator.validate_add_flight_request(request)
    if request_validation_response.value:
        flight = FlightDataValidator.create_chronometer_object(request)
        chrono_validation_response = FlightDataValidator.validate_chrono_table(flight)
        if chrono_validation_response.value:
            flight.save()
    else:
        print(request_validation_response.content)
    return redirect('index')


def start_flight(request):
    if request.method == 'GET':
        return redirect('index')

    if len(request.form) == 1:
        id = next(iter(request.form))
        flight = Chronometer.objects.filter(flight_nr=int(id)).first()
        validate_chrono_response = FlightDataValidator.validate_chrono_for_start(flight)
        if validate_chrono_response.value:
            flight.time_of_start = str(datetime.datetime.now())[11:16]
            if flight.airplane:
                airplane_flight = chrono_to_airplane(flight)
                airplane_flight.save()
            flight.active = True
        else:
            print(validate_chrono_response.content)
    return redirect('index')


def stop_flight(request):
    if request.method != 'POST':
        return redirect('index')
    if len(request.form) == 1:
        id = next(iter(request.form))
        main_flight = Chronometer.objects.filter(flight_nr=int(id[1:])).first()
        timedif = time_difference(main_flight.time_of_start,
                                  str(datetime.datetime.now())[11:16])

        if id.startswith("g"):
            main_flight.glider_landing_time = str(datetime.datetime.now())[11:16]
            main_flight.glider_tia = timedif
            main_flight.active = False
            main_flight.glider.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            main_flight.save()
        elif id.startswith("a"):
            airplane_flight = AirplaneFlight.objects.filter(flight_nr=int(id[1:])
                                                            ).first()
            main_flight.airplane_landing_time = str(datetime.datetime.now())[
                                                11:16]
            main_flight.airplane_tia = timedif
            airplane = Airplane.objects.filter(name=airplane_flight.airplane).first()
            airplane.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            airplane_flight.delete()
    return redirect('index')


def delete_flight(request):
    if request.method == 'GET':
        return redirect('index')
    if len(request.form) == 1:
        id = next(iter(request.form))
        Chronometer.objects.filter(flight_nr=id).first().delete()
    return redirect('index')


def delete(request):
    table = models_dictionary.get(request.GET.get('table'))
    obj = table.objects.filter(id=request.GET.get('id')).first()
    print('does it work:', request.GET.get('id'))
    obj.delete()
    return redirect('manage')


def update(request):
    if request.method == 'GET':
        return redirect('index')
    arguments = {argument: request.POST.get(argument) for argument in request.POST if argument != 'csrfmiddlewaretoken'}
    flip_booleans(arguments)
    table = models_dictionary.get(request.GET.get('table'))
    table.objects.filter(id=request.POST.get('id')).update(**arguments)
    print(arguments)
    return redirect('manage')


def add(request):
    if request.method == 'GET':
        return redirect('manage')
    table = models_dictionary.get(request.GET.get('table'))
    arguments = {argument: request.POST.get(argument) for argument in request.POST if argument != 'csrfmiddlewaretoken'}
    flip_booleans(arguments)
    print(arguments)

    table(**arguments).save()
    return redirect('manage')
