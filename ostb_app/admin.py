from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Category)
admin.site.register(models.Poster)
admin.site.register(models.Location)
admin.site.register(models.Event)
admin.site.register(models.TicketType)
admin.site.register(models.Ticket)
admin.site.register(models.Payment)