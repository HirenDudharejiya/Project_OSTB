from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import UserProfile,Event
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from .forms import PurchaseTicketForm
from django.contrib import messages 

# Create your views here.

#views for index page--
def index(request):
    return render(request,"index.html")

# views for events
def events(request):
    events = Event.objects.all()  
    return render(request, "shows_events.html", {"events": events})

#views for events list
def event_list(request):
    events_obj = Event.objects.all()
    return render(request, "event-details.html", {"events_list": events_obj})



# views for about page
def about(request):
    return render(request,"about.html")

# views for tickets
def tickets(request):
    events = Event.objects.all()
    return render(request, 'tickets.html', {'events': events})

# views for ticket-details
def ticket_details(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'ticket-details.html', {'event': event})

#views for Customer-Regiter
@csrf_exempt 

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        usertype = request.POST.get('usertype')

        usern = User.objects.filter(username=username).first()
        usere = User.objects.filter(email=email).first()

        if usern:
            messages.error(request, "Username already exists, please provide a different username")
        elif usere:
            messages.error(request, "Email already exists, please provide a different email")
        elif password != confirmpassword:
            messages.error(request, "Password and confirm password do not match")
        else:
            try:
                # Create the user
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    password=password
                )

                profile = UserProfile(
                    date_of_birth=date_of_birth, 
                    mobile_no=mobile_no, 
                    usertype=usertype, 
                    users_model=user
                )
                profile.save() 
                messages.success(request, "Registration successful! You can now log in.")
                return redirect("user_login") 
            
            except Exception as e:
                messages.error(request, f"An error occurred while saving your profile: {e}")

    return render(request, "user_register.html")


def user_login(request):
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        usert = UserProfile.objects.filter(users_model=user).first() if user else None

        if user and usert:
            if usert.usertype == usertype:
                login(request, user)
                if usert.usertype == "Customer":
                    return redirect("index")
                else:
                    return redirect("org_index")
            else:
                messages.error(request, "User type does not match.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "user_login.html")

#Views for user-profile
def user_profile(request, username):
    # usern = User.objects.filter(username=username).first()
    return render(request,"user-profile.html")

# Views for user-Logout
@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect("index")

# Views for organizer index
def org_index(request):
    return render(request,"organizer/org-index.html")

# Views for organizer profile
def org_profile(request):
    organizer = get_object_or_404(UserProfile, user=request.id)
    events = Event.objects.filter(organizer=organizer)
    
    context = {
        'organizer': organizer,
        'events': events,
    }

    return render(request,"organizer/org-profile.html", context)

#Views for add events
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_startdate = request.POST.get('event_startdate')
        event_enddate = request.POST.get('event_enddate')
        ticket_price = request.POST.get('ticket_price')
        quantity = request.POST.get('quantity')
        image = request.POST.get('image')
        line1 = request.POST.get('line1')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        state = request.POST.get('state')

        event = Event(event_name = event_name, 
                      event_description = event_description, 
                      event_startdate = event_startdate, 
                      event_enddate = event_enddate,
                      ticket_price = ticket_price,
                      quantity = quantity,
                      image = image,
                      line1 = line1,
                      zipcode = zipcode,
                      city = city,
                      state = state)
        event.save()
         
        return redirect("payment_details")
    return render(request,"organizer/add-event.html")

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'organizer/event_confirm_delete.html'  
    success_url = reverse_lazy('events')

# def purchase_ticket(request, ticket_id):
#     ticket = get_object_or_404(Event, id=ticket_id)

#     if request.method == 'POST':
#         form = PurchaseTicketForm(request.POST)
#         if form.is_valid():
#             quantity = form.cleaned_data['quantity']

#             if quantity <= ticket.available_tickets:
#                 # Process the purchase (deduct tickets)
#                 ticket.available_tickets -= quantity
#                 ticket.save()
                
#                 messages.success(request, f'You have successfully purchased {quantity} tickets for {ticket.event.event_name}!')
#                 return redirect('ticket_success')  # Redirect to a success page
#             else:
#                 messages.error(request, 'Not enough tickets available.')
#     else:
#         form = PurchaseTicketForm()

#     return render(request, 'purchase_ticket.html', {
#         'form': form,
#         'ticket': ticket,
#     })

#Views for payment details
def payment_details(request):
    return render(request,"organizer/payment-details.html")