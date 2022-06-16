from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/',views.manage,name='manage'),
    path('add',views.add,name='add'),
    path('delete',views.delete,name='delete'),
    path('update',views.update,name='update'),
    path('add_flight', views.add_flight, name='add_flight')
]