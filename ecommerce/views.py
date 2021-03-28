from decimal import Decimal
from typing import Optional, Dict

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ecommerce.models import Ticket, Order
from user.models import User


@login_required(login_url='user/login')
def home(request):
    tickets = Ticket.objects.filter(orders__isnull=True)
    user = User.objects.get(id=request.user.id)
    user_balance = user.balance
    ticket_orders_info: Dict[str, Optional[Decimal]] = user.orders.all().aggregate(
        paid_last_year=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=365))),
        bought_last_year=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=365))),
        paid_last_month=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(weeks=4))),
        bought_last_month=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(weeks=4))),
        paid_last_week=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=7))),
        bought_last_week=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=7)))
    )

    page = request.GET.get('page', 1)
    paginator = Paginator(tickets, 12)
    try:
        tickets_pag = paginator.page(page)
    except PageNotAnInteger:
        tickets_pag = paginator.page(1)
    except EmptyPage:
        tickets_pag = paginator.page(paginator.num_pages)

    return render(request, 'pages/home.html',
                  {'tickets': tickets,
                   **ticket_orders_info,
                   'tickets_count': tickets.count(),
                   'user_balance': user_balance,
                   'tickets_pag': tickets_pag})


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
                                                       'orders_count': orders_count + 1,
                                                       'user_balance': user.balance})


def profile(request):
    orders = User.objects.get(id=request.user.id).orders.all()
    user = User.objects.get(id=request.user.id)
    user_balance = user.balance

    tickets_q = Q()
    q = request.GET.get('q')
    if q:
        tickets_q &= Q(ticket__name__contains=q)

    ticket_orders_info: Dict[str, Optional[Decimal]] = user.orders.all().aggregate(
        paid_last_year=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=365))),
        bought_last_year=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=365))),
        paid_last_month=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(weeks=4))),
        bought_last_month=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(weeks=4))),
        paid_last_week=Sum('price', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=7))),
        bought_last_week=Count('id', filter=Q(order_date__gte=timezone.now() - timezone.timedelta(days=7)))
    )

    return render(request, 'pages/profile.html', {'orders': orders.filter(tickets_q),
                                                  'orders_count': orders.count(),
                                                  'user_balance': user_balance,
                                                  **ticket_orders_info})
