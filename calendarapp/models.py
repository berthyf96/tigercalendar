# python manage.py makemigrations polls
# By running makemigrations, youre telling Django that
# youve made some changes to your models and that youd
# like the changes to be stored as a migration.

# 1) make changes here
# 2) python manage.py makemigrations
# 3) python manage.py migrate

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
import arrow

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

DEFAULT_ID = 1

class Event(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, default=DEFAULT_ID)
    category = models.ManyToManyField(Category, default=DEFAULT_ID)
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=100, null=True, blank=True)  # Better field type?
    is_free = models.BooleanField(default=False)
    website = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_datetime >= self.end_datetime:
            raise ValidationError('Ending times must after starting times')

class User(models.Model):
    email = models.CharField(max_length=100, default = '')
    password = models.CharField(max_length=100, default = '')
    first_name = models.CharField(max_length=100, default = '')
    last_name = models.CharField(max_length=100, default = '')
    favorite_events = models.ManyToManyField(Event, related_name = 'fav_events')
    admin = models.BooleanField(default=False)
    my_events = models.ManyToManyField(Event, related_name = 'my_events')
    my_orgs = models.ManyToManyField(Organization)

    def __str__(self):
        return self.username

class Appointment(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    time = models.DateTimeField()


    # Additional fields not visible to users
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        appointment_time = arrow.get(self.time, self.time_zone.zone)

        if appointment_time < arrow.utcnow():
            raise ValidationError(
                'You cannot schedule an appointment for the past. '
                'Please check your time and time_zone')

    def schedule_reminder(self):
        """Schedule a Dramatiq task to send a reminder for this appointment"""

        # Calculate the correct time to send this reminder
        appointment_time = arrow.get(self.time)
        reminder_time = appointment_time.shift(minutes=-1440)
        now = arrow.now()
        milli_to_wait = int(
            (reminder_time - now).total_seconds()) * 1000

        # Schedule the Dramatiq task
        from .tasks import send_sms_reminder
        result = send_sms_reminder.send_with_options(
            args=(self.pk,),
            delay=milli_to_wait)

        return result.options['redis_message_id']

    def save(self, *args, **kwargs):
        """Custom save method which also schedules a reminder"""

        # Check if we have scheduled a reminder for this appointment before
        if self.task_id:
            # Revoke that task in case its time has changed
            self.cancel_task()

        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        super(Appointment, self).save(*args, **kwargs)

        # Schedule a new reminder task for this appointment
        self.task_id = self.schedule_reminder()

        # Save our appointment again, with the new task_id
        super(Appointment, self).save(*args, **kwargs)
