from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#----Models for Customer & Sports Dealer----
USER_TYPE = [("Customer","Customer"),
             ("Event_organizer","Event_organizer")]

class UserProfile(models.Model):
    date_of_birth = models.DateField()
    mobile_no = models.BigIntegerField()
    user_type = models.CharField(choices = USER_TYPE,max_length=20)
    users_model = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "UserProfile"


#---Models for Event Details---
class Event(models.Model):
    event_name = models.CharField(max_length = 50)
    event_description = models.TextField(max_length = 120)
    event_startdate = models.DateTimeField()
    event_enddate = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Event"

class Category(models.Model):
    category_name = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default='')

    class Meta:
        verbose_name_plural = "Category"

class Poster(models.Model):
    poster_image = models.ImageField()
    banner_image = models.ImageField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default='')

    class Meta:
        verbose_name_plural = "Poster"

class Location(models.Model):
    line1 = models.CharField('line1', max_length=50)
    line2 = models.CharField('line2', max_length=50)
    zip_code = models.IntegerField()
    city = models.CharField('city', max_length=50)
    state = models.CharField('state', max_length=50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default='')

    class Meta:
        verbose_name_plural = "Location"


#---Models for Tickets--- 
class TicketType(models.Model):
    ticket_type = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "TicketType"

class Ticket(models.Model):
    ticket_price = models.FloatField()
    discount = models.FloatField()
    quantity = models.IntegerField()
    returnable = models.BooleanField(default=False)
    return_condition = models.CharField(max_length=50)
    user_model = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Ticket"

#---Models for Payment---

class Payment(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=10)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=10)
    amount = models.FloatField()
    acknowledgement_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    user_model = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Payment"