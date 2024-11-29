# Generated by Django 4.2.6 on 2024-11-29 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50)),
                ('event_description', models.TextField()),
                ('event_startdate', models.DateTimeField()),
                ('event_enddate', models.DateTimeField()),
                ('ticket_price', models.FloatField()),
                ('quantity', models.PositiveIntegerField()),
                ('available_tickets', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(default='path/to/default/image.jpg', upload_to='events/images/')),
                ('line1', models.CharField(default='Default Address', max_length=50)),
                ('zipcode', models.CharField(default='000000', max_length=10)),
                ('city', models.CharField(default='Default City', max_length=50)),
                ('state', models.CharField(default='Default State', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Event',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('mobile_no', models.CharField(max_length=15)),
                ('usertype', models.CharField(choices=[('Customer', 'Customer'), ('Event_organizer', 'Event_organizer')], default='default_value', max_length=20)),
                ('users_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('acknowledgement_no', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('event_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ostb_app.event')),
                ('user_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ostb_app.userprofile')),
            ],
            options={
                'verbose_name_plural': 'Payment',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ostb_app.userprofile'),
        ),
    ]
