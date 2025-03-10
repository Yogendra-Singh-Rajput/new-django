from django.urls import path, include, re_path
from .views import home,search,contact_us
urlpatterns = [
    path('',home,name='Home'),
    path('numerology/',include('numerology.urls'), name= 'numerology'),
    path('search/',search,name='Search'),
    path('contact_us/',contact_us)
]