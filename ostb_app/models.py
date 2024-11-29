from django.db import models
from django.contrib.auth.models import User

# Models for Customer & Event_organizer
USER_TYPE = [("Customer","Customer"),
            ("Event_organizer","Event_organizer")]

TICKET_TYPE = [("Paid","Paid"),
               ("Free","Free")]

class UserProfile(models.Model):
    users_model = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    mobile_no = models.CharField(max_length=15)
    usertype = models.CharField(choices=USER_TYPE, max_length=20, default='default_value')

    def __str__(self):
        return self.users_model.username    

# Models for Event Details
class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.TextField()
    event_startdate = models.DateTimeField()
    event_enddate = models.DateTimeField()
    ticket_price = models.FloatField()
    quantity = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    image = models.ImageField(upload_to='events/images/', default='path/to/default/image.jpg')
    line1 = models.CharField(max_length=50, default='Default Address')
    zipcode = models.CharField(max_length=10, default='000000')
    city = models.CharField(max_length=50, default='Default City')
    state = models.CharField(max_length=50, default='Default State')
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # This is the foreign key for organizer

    class Meta:
        verbose_name_plural = "Event"

    def __str__(self):
        return self.event_name
    
    @property
    def location(self):
        # Combine the fields into a single string
        return f"{self.line1}, {self.city}, {self.state}, {self.zipcode}"

# Models for Payment
class Payment(models.Model):
    amount = models.FloatField()
    acknowledgement_no = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    user_model = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event_model = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Payment"

    def __str__(self):
        return f"Payment {self.acknowledgement_no} - {self.status}"