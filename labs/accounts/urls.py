from django.urls import path

from . import views
from accounts.views import *

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("<int:id>", views.user_page, name='user_page'),
    path("login", views.log_in, name='login')
]

handler404 = 'accounts.views.handle404'
