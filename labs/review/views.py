from django.http import HttpResponse
from django.shortcuts import render, redirect
from echrono.models import AirplaneTechnicalReview, Airplane, User, Glider, \
    GliderTechnicalReview

from echrono.FlightDataValidator import *

def index(request):
    if request.method == "POST":
        print('happens')
        print(request.POST)
        if 'airplane' in request.POST:
            return redirect('airplane/' + request.POST.get('airplane'))

        if 'glider' in request.POST:
            return redirect('glider/' + request.POST.get('glider'))

    return render(request, 'review/index.html',
                  {"airplanes": Airplane.objects.all(),
                   "gliders": Glider.objects.all()})


def glider(request):
    if request.method == "POST":
        return redirect('glider/' + request.POST.get('glider'))
    return render(request, 'review/glider.html',
                  {"gliders": Glider.objects.all()})


def airplane(request):
    if request.method == "POST":
        return redirect('airplane/' + request.POST.get('airplane'))
    return render(request, 'review/airplane.html',
                  {"airplanes": Airplane.objects.all()})


def glider_review(request, id):
    if request.method == "POST":
        arguments = {argument: request.POST.get(argument) for argument in
                     request.POST if argument != 'csrfmiddlewaretoken'}
        flip_booleans(arguments)



        GliderTechnicalReview(
            date=datetime.datetime.now(),
            inspector_id=User.objects.filter(id=request.POST.get('inspector')).first(),
            glider_id=Glider.objects.filter(id=id).first(),
            wings_check=arguments.get('wings'),
            fuselage_check=arguments.get('fuselage'),
            sheathing_check=arguments.get('sheathing')).save()

    return render(request, 'review/glider_review.html',
                  {"glider": Glider.objects.filter(id=id).first(),
                   "inspectors": User.objects.filter(inspector=True).all(),
                   "glider_reviews": GliderTechnicalReview.objects.filter(
                       glider_id=Glider.objects.filter(id=id).first()).all()})


def airplane_review(request, id):
    if request.method == "POST":
        arguments = {argument: request.POST.get(argument) for argument in
                     request.POST if argument != 'csrfmiddlewaretoken'}
        flip_booleans(arguments)

        AirplaneTechnicalReview(
            date=datetime.datetime.now(),
            inspector_id=User.objects.filter(id=arguments.get('inspector')).first(),
            airplane_id=Airplane.objects.filter(id=id).first(),
            engine_check=arguments.get('engine'),
            fuselage_check=arguments.get('fuselage'),
            sheathing_check=arguments.get('sheathing')).save()

    return render(request, 'review/airplane_review.html',
                  {"airplane": Airplane.objects.filter(id=id).first(),
                   "inspectors": User.objects.filter(inspector=True).all(),
                   "airplane_reviews": AirplaneTechnicalReview.objects.filter(
                       airplane_id=Airplane.objects.filter(
                           id=id).first()).all()})
