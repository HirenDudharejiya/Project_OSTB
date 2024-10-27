from django import forms

class PurchaseTicketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Number of Tickets')
