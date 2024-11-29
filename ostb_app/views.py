from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import Event, UserProfile, Payment
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa 

def index(request):
    return render(request, "index.html")

def events(request):
    events_list = Event.objects.all()
    paginator = Paginator(events_list, 6)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    return render(request, "shows-events.html", {"events": events})

def event_list(request, organizer_id):
    organizer = get_object_or_404(UserProfile, id=organizer_id)
    events = Event.objects.filter(organizer=organizer)
    return render(request, 'event_list.html', {'organizer': organizer, 'events': events})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'ticket-details.html', {'event': event})

def about(request):
    return render(request, "about.html")

def tickets(request):
    events = Event.objects.all()
    return render(request, "tickets.html", {"events": events})

@csrf_exempt
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile_no = request.POST.get("mobile_no")
        date_of_birth = request.POST.get("date_of_birth")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        usertype = request.POST.get("usertype")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose a different email.")
        elif password != confirmpassword:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    password=password
                )
                UserProfile.objects.create(
                    users_model=user,
                    date_of_birth=date_of_birth,
                    mobile_no=mobile_no,
                    usertype=usertype
                )
                messages.success(request, "Registration successful! You can now log in.")
                return redirect("user_login")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    return render(request, "user_register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        usertype = request.POST.get("usertype")

        user = authenticate(request, username=username, password=password)
        if user:
            profile = UserProfile.objects.filter(users_model=user).first()
            if profile and profile.usertype == usertype:
                login(request, user)
                return redirect("index" if usertype == "Customer" else "org_index")
            else:
                messages.error(request, "User type mismatch.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "user_login.html")

@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect("index")

def org_index(request):
    organizers = UserProfile.objects.filter(
        usertype="Event_organizer", 
        users_model__isnull=False
    ).select_related('users_model')
    return render(request, "organizer/org-index.html", {"organizers": organizers})

def org_profile(request, id):
    organizer = get_object_or_404(UserProfile, users_model__id=id, usertype="Event_organizer")
    events = Event.objects.filter(organizer=organizer)
    context = {
        "organizer": organizer,
        "events": events,
    }
    return render(request, "organizer/org-profile.html", context)

def organizer_events(request):
    user = request.user
    events = Event.objects.filter(organizer=user)
    context = {
        'events': events
    }
    return render(request, 'organizer/events_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {'event': event}
    return render(request, 'organizer/event_detail.html', context)

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        pass
    return render(request, 'organizer/edit_event.html', {'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('organizer_events')

@login_required
def add_event(request):
    if request.method == "POST":
        event_name = request.POST['event_name']
        event_description = request.POST['event_description']
        event_startdate = request.POST['event_startdate']
        event_enddate = request.POST['event_enddate']
        ticket_price = request.POST['ticket_price']
        quantity = request.POST['quantity']
        image = request.FILES['image']
        line1 = request.POST['line1']
        zipcode = request.POST['zipcode']
        city = request.POST['city']
        state = request.POST['state']

        organizer = request.user.userprofile

        event = Event.objects.create(
            event_name=event_name,
            event_description=event_description,
            event_startdate=event_startdate,
            event_enddate=event_enddate,
            ticket_price=ticket_price,
            quantity=quantity,
            available_tickets=quantity,
            image=image,
            line1=line1,
            zipcode=zipcode,
            city=city,
            state=state,
            organizer=organizer
        )

        return redirect('org_index')

    return render(request, 'organizer/add-event.html')

class EventDeleteView(DeleteView):
    model = Event
    template_name = "organizer/event_confirm_delete.html"
    success_url = reverse_lazy("events")

@login_required
def purchase_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.available_tickets <= 0:
        return render(request, "error.html", {"message": "No tickets available for this event."})

    if request.method == "POST":
        user_profile = request.user.userprofile
        num_tickets = int(request.POST.get('num_tickets', 1))
        total_amount = event.ticket_price * num_tickets

        payment = Payment.objects.create(
            amount=total_amount,
            acknowledgement_no=f"ACK-{event.id}-{request.user.id}",
            status="Completed",
            user_model=user_profile,
            event_model=event,
        )

        event.available_tickets -= num_tickets
        event.save()

        return redirect("payment_success", payment_id=payment.id)

    return render(request, "purchase_ticket.html", {"event": event})

@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payment_success.html", {"payment": payment})

@login_required
def purchased_tickets(request):
    payments = Payment.objects.filter(user_model=request.user.userprofile)
    return render(request, 'purchased_tickets.html', {'payments': payments})

def download_ticket(request, payment_id):
    payment = Payment.objects.get(id=payment_id)

    context = {
        'payment': payment,
        'event': payment.event_model,
        'user': payment.user_model,
        'ticket_quantity': payment.amount // payment.event_model.ticket_price
    }

    html = render_to_string('ticket_pdf_template.html', context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{payment_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)

    return response
