from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('airplane', views.airplane, name='glider'),
    path('glider', views.airplane, name='glider'),
    path('glider/<int:id>', views.airplane, name='glider'),
    path('airplane/<int:id>', views.glider, name='airplane')
]
