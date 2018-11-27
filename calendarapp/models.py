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
