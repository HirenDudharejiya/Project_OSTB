from django import template
register = template.Library()

@register.filter
def calculate_tickets(amount, ticket_price):
    total_tickets = int(amount // ticket_price) 
    try:
        return total_tickets
    except (TypeError, ZeroDivisionError):
        return 0