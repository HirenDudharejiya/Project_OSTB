from django.urls import path
from . import views
from .views import EventDeleteView

urlpatterns = [
    path('',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_register/',views.user_register,name='user_register'),
    path('logout/', views.user_logout, name='logout'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('event_list/',views.event_list,name='event_list'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('events/',views.event_list,name='events'),
    path('about/',views.about,name='about'),
    path('tickets/', views.tickets, name='tickets'),
    path('ticket_details/<int:id>/', views.ticket_details, name='ticket_details'),
    path('org_index/',views.org_index,name='org_index'),
    path('org_profile/',views.org_profile,name='org_profile'),
    path('add_event/',views.add_event,name='add_event'),
    path('payment_details/',views.payment_details,name='payment_details'),
]