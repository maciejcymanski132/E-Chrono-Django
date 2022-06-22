from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.pod, name='pod')
]

handler404 = 'accounts.views.handle404'
handler500 = 'accounts.views.handle500'
