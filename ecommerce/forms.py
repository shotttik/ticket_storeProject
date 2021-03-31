from django import forms

from ecommerce.models import Ticket


class TicketForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control',
        }
    ))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'class': 'form-control',
        }
    ))
    barcode = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = Ticket
        fields = ('name', 'start_date', 'end_date', 'barcode')
