from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_register/',views.user_register,name='user_register'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('event_list/',views.event_list,name='event_list'),
    path('events/',views.events,name='events'),
    path('about/',views.about,name='about'),
    path('tickets/',views.tickets,name='tickets'),
    path('ticket_details/',views.ticket_details,name='ticket_details'),
    path('org_index/',views.org_index,name='org_index'),
    path('org_profile/',views.org_profile,name='org_profile'),
    path('add_event/',views.add_event,name='add_event'),
    path('add_img/',views.add_img,name='add_img'),
    path('add_location/',views.add_location,name='add_location'),
    path('add_ticket/',views.add_ticket,name='add_ticket'),
    path('return_ticket/',views.return_ticket,name='return_ticket'),
    path('payment_details/',views.payment_details,name='payment_details'),

    
]