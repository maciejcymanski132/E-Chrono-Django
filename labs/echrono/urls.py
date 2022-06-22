from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/', views.manage, name='manage'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete'),
    path('update', views.update, name='update'),
    path('add_flight', views.add_flight, name='add_flight'),
    path('start_flight', views.start_flight, name='start_flight'),
    path('stop_flight', views.stop_flight, name='stop_flight'),
    path('delete_flight', views.delete_flight, name='delete_flight')
]

handler404 = 'accounts.views.handle404'
handler500 = 'accounts.views.handle500'
