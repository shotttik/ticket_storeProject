from django.urls import path
from ecommerce.views import home

urlpatterns = [
    path('', home, name='home')
]