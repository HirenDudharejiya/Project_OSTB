from django.urls import path
from . import views
from .views import EventDeleteView

urlpatterns = [
    path('',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_register/',views.user_register,name='user_register'),
    path('logout/', views.user_logout, name='logout'),
    path('event/<int:id>/', views.event_detail, name='event_detail'), 
    path('purchase-ticket/<int:event_id>/', views.purchase_ticket, name='purchase_ticket'),
    path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('purchased-tickets/', views.purchased_tickets, name='purchased_tickets'),
    path('events/', views.events, name='events'), 
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('organizer/events/', views.organizer_events, name='organizer_events'),
    path('about/',views.about,name='about'),
    path('tickets/', views.tickets, name='tickets'),
    path("org_index/", views.org_index, name="org_index"),
    path("org_profile/<int:id>/", views.org_profile, name="org_profile"),
    path('add_event/',views.add_event,name='add_event'),
    path('download-ticket/<int:payment_id>/', views.download_ticket, name='download_ticket'),
]