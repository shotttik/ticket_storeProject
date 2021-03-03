from django.db import models
from user.models import User


class Ticket(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    start_date = models.DateTimeField(verbose_name='Start Date')
    end_date = models.DateTimeField(verbose_name='End Date')
    barcode = models.CharField(verbose_name="Barcode", max_length=15, unique=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'


class Order(models.Model):
    price = models.DecimalField(verbose_name="Order Price", max_digits=6, decimal_places=2, default=0,
                                help_text='In USD')
    order_date = models.DateTimeField(verbose_name='Order Date', auto_now=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.user} - {self.ticket}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
