from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile,Event,Poster,Location
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#views for index page--
def index(request):
    return render(request,"index.html")

#views for events list
def event_list(request):
    return render(request,"event-details.html")

#views for events
def events(request):
    return render(request,"shows-events.html")

# views for about page
def about(request):
    return render(request,"about.html")

# views for tickets
def tickets(request):
    return render(request,"tickets.html")

# views for ticket-details
def ticket_details(request):
    return render(request,"ticket-details.html")

#views for Customer-Regiter
@csrf_exempt  #CSRF Decorator
def user_register(request):
    message=""
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

        # usert = UserProfile.objects.filter(users_model=user).first()

        if usern:
            message = "Username already exists, please provide a different username"
        elif usere:
            message = "Email already exists, please provide a different email"
        elif password != confirmpassword:
            message = "Password and confirm password does not matches"
        else:
            user = User.objects.create_user( username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            profile = UserProfile(date_of_birth=date_of_birth, mobile_no=mobile_no, user_type=usertype, users_model=user)

            user.save()
            profile.save()

        if usertype == "Customer":
            return redirect("index")
        else:
            return redirect("org_index")
        
    return render(request,"user_register.html")

# views for Customer-Login  
def user_login(request):
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        usert = UserProfile.objects.filter(users_model=user).first()

        if user and usert.user_type == usertype:
            login(request, user)
            if usert == "Customer":
                return redirect("index")
            else:
                return redirect("org_index")

    return render(request,"user_login.html")

#Views for user-profile
def user_profile(request, username):
    # usern = User.objects.filter(username=username).first()
    return render(request,"user-profile.html")

# Views for user-Logout
@csrf_exempt
def user_logout(request):
    logout(request)
    return render(request,"index.html")

# Views for organizer index
def org_index(request):
    return render(request,"organizer/org-index.html")

# Views for organizer profile
def org_profile(request):
    return render(request,"org-profile.html")

#Views for add events
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        # category_name = request.POST.get('category_name')
        event_description = request.POST.get('event_description')
        event_startdate = request.POST.get('event_startdate')
        event_enddate = request.POST.get('event_enddate')

        event = Event(event_name = event_name, event_description = event_description, event_startdate = event_startdate, event_enddate = event_enddate)
        event.save()
         
        return redirect("add_img")
    return render(request,"organizer/add-event.html")

#Views for add Poster images
@csrf_exempt
def add_img(request):
    if request.method == "POST":
        poster_image = request.FILES.get('poster_image')
        banner_image = request.FILES.get('banner_image')

        img_obj = Poster.objects.create(poster_image=poster_image,banner_image=banner_image,)
        img_obj.save()

        return redirect("add_location")
        
    return render(request,"organizer/add-img.html")

#Views for add Location
@csrf_exempt
def add_location(request):
    if request.method == "POST":
        line1 = request.POST.get('line1')
        line2 = request.POST.get('line2')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        state = request.POST.get('state')

        location = Location(line1 = line1, line2 = line2, zip_code = zip_code, city = city, state = state)
        location.save()

        return redirect("add_ticket")

    return render(request,"organizer/add-location.html")

#Views for add Ticket Details
@csrf_exempt
def add_ticket(request):
    return render(request,"organizer/add-ticket-details.html")

#Views for add Return-Ticket
def return_ticket(request):
    return render(request,"organizer/return-ticket-info.html")

#Views for payment details
def payment_details(request):
    return render(request,"organizer/payment-details.html")