from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ecommerce.models import Ticket


@login_required(login_url='user/login')
def home(request):
    tickets = Ticket.objects.filter(orders__isnull=True)
    return render(request, 'pages/home.html',
                  {'tickets': tickets})
