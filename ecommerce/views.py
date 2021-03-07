from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ecommerce.models import Ticket, Order
from user.models import User


@login_required(login_url='user/login')
def home(request):
    tickets = Ticket.objects.filter(orders__isnull=True)
    return render(request, 'pages/home.html',
                  {'tickets': tickets})


@login_required(login_url='user/login')
def ticket_order(request, pk: int):
    ticket: Ticket = get_object_or_404(Ticket.objects.filter(orders__isnull=True), pk=pk)
    time_now = timezone.now()
    user = User.objects.get(id=request.user.id)
    orders_count = user.orders.count()
    if request.method == 'POST':
        if user.balance >= Decimal(request.POST['price']):
            order = Order.objects.create(ticket_id=pk,
                                         user_id=request.user.id)
            order.price = Decimal(request.POST['price'])
            user.balance = user.balance - Decimal(request.POST['price'])
            user.save()
            order.save()
            return redirect('home')
        else:
            error = "You don't have enough balance. Please fill and try again!"
            return render(request, 'pages/ticket_order.html', {'ticket': ticket,
                                                               'time_now': time_now,
                                                               'error': error})
    return render(request, 'pages/ticket_order.html', {'ticket': ticket,
                                                       'time_now': time_now,
                                                       'user': user,
                                                       'orders_count': orders_count})


def profile(request):
    orders = User.objects.get(id=request.user.id).orders.all()
    return render(request, 'pages/profile.html', {'orders': orders})
