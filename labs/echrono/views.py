from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from .FlightDataValidator import *
from .models import *

models_dictionary = {
    'Glider': Glider,
    'Airplane': Airplane,
    'User': User
}


def index(request):
    if request.user.is_authenticated:
        context = {
            'chrono': Chronometer.objects.all(),
            'airplanes': Airplane.objects.all(),
            'gliders': Glider.objects.all(),
            'users': User.objects.all(),
            'airplane_flights': AirplaneFlight.objects.all()
        }
        return render(request, 'echrono/index.html', context)
    return redirect('home')


def manage(request):
    if request.user.is_authenticated:
        context = {
            'airplanes': Airplane.objects.all(),
            'gliders': Glider.objects.all(),
            'users': User.objects.all()
        }
        return render(request, 'echrono/manage.html', context)
    return redirect('home')


def add_flight(request):
    print(request.POST)
    if request.user.is_authenticated:
        request_validation_response = FlightDataValidator.validate_add_flight_request(request)

        if request_validation_response.value:
            flight = FlightDataValidator.create_chronometer_object(request)
            chrono_validation_response = FlightDataValidator.validate_chrono_table(flight)
            if chrono_validation_response.value:
                flight.save()
        return redirect('/echrono')
    return redirect('manage')


def start_flight(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return redirect('index')
        arguments = {argument: request.POST.get(argument) for argument in request.POST if
                     argument != 'csrfmiddlewaretoken'}
        if len(arguments) == 1:

            id = next(iter(arguments))
            flight = Chronometer.objects.filter(id=int(id)).first()
            validate_chrono_response = FlightDataValidator.validate_chrono_for_start(flight)
            if validate_chrono_response.value:
                flight.time_of_start = timezone.now()
                if flight.airplane_id:
                    airplane_flight = chrono_to_airplane(flight)
                    airplane_flight.save()
                flight.active = True
                flight.save()
            else:
                print(validate_chrono_response.content)
        return redirect('/echrono')
    return redirect('home')


def stop_flight(request):
    if request.user.is_authenticated:
        if request.method != 'POST':
            return redirect('index')
        arguments = {argument: request.POST.get(argument) for argument in request.POST if
                     argument != 'csrfmiddlewaretoken'}
        if len(arguments) == 1:
            id = next(iter(arguments))
            main_flight = Chronometer.objects.filter(id=int(id[1:])).first()
            timedif = time_difference(main_flight.time_of_start,
                                      timezone.now())

            if id.startswith("g"):
                main_flight.glider_landing_time = timezone.now()
                main_flight.glider_tia = timedif
                main_flight.active = False

                if main_flight.glider_id.time_in_air:
                    main_flight.glider_id.time_in_air += int(timedif.seconds / 60)
                else:
                    main_flight.glider_id.time_in_air = int(timedif.seconds / 60)
                main_flight.glider_id.save()
                main_flight.save()

            elif id.startswith("a"):
                airplane_flight = AirplaneFlight.objects.filter(id=int(id[1:])
                                                                ).first()
                main_flight.airplane_landing_time = timezone.now()
                main_flight.airplane_tia = timedif
                airplane = Airplane.objects.filter(name=airplane_flight.airplane.name).first()
                if airplane.time_in_air:
                    airplane.time_in_air += int(timedif.seconds / 60)
                else:
                    airplane.time_in_air = int(timedif.seconds / 60)
                airplane.save()
                main_flight.save()
                airplane_flight.delete()
        return redirect('/echrono')
    return redirect('home')


def delete_flight(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return redirect('index')
        arguments = {argument: request.POST.get(argument) for argument in request.POST if
                     argument != 'csrfmiddlewaretoken'}
        if len(arguments) == 1:
            id = next(iter(arguments))
            Chronometer.objects.filter(id=id).first().delete()
        return redirect('/echrono')
    return render(request, 'home.html')


def delete(request):
    if request.user.is_authenticated:
        table = models_dictionary.get(request.GET.get('table'))
        obj = table.objects.filter(id=request.GET.get('id')).first()
        obj.delete()
        return redirect('manage')
    return redirect('home')


def update(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return redirect('index')
        arguments = {argument: request.POST.get(argument) for argument in request.POST if
                     argument != 'csrfmiddlewaretoken'}
        flip_booleans(arguments)
        table = models_dictionary.get(request.GET.get('table'))
        table.objects.filter(id=request.POST.get('id')).update(**arguments)
        return redirect('manage')
    return redirect('home')


def add(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return redirect('manage')
        table = models_dictionary.get(request.GET.get('table'))
        arguments = {argument: request.POST.get(argument) for argument in request.POST if
                     argument != 'csrfmiddlewaretoken'}
        flip_booleans(arguments)
        table(**arguments).save()
        return redirect('manage')
    return redirect('home')
