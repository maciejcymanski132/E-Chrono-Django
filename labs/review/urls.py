from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('airplane', views.airplane, name='glider'),
    path('glider', views.glider, name='glider'),
    path('glider/<int:id>', views.glider_review, name='glider'),
    path('airplane/<int:id>', views.airplane_review, name='airplane')
]

handler404 = 'accounts.views.handle404'
