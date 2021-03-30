from django.urls import path
from ecommerce.views import home, ticket_order, profile, add_ticket, del_ticket

urlpatterns = [
    path('', home, name='home'),
    path('order/ticket/<int:pk>', ticket_order, name='ticket_order'),
    path('profile/', profile, name='profile'),
    path('add/ticket', add_ticket, name='add_ticket'),
    path('del-ticket/<int:pk>', del_ticket, name='del_ticket')
]
