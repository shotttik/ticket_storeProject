from django.urls import path
from ecommerce.views import home, ticket_order, profile

urlpatterns = [
    path('', home, name='home'),
    path('order/ticket/<int:pk>', ticket_order, name='ticket_order'),
    path('profile/', profile, name='profile')
]
