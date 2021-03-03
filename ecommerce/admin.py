from django.contrib import admin
from ecommerce.models import Ticket, Order


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
