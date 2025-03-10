from django.urls import path
from .views import *
urlpatterns = [
    path('',home),
    path('app1/', app1),
    path('app2/',app2),
    path('app3/',app3)
]
