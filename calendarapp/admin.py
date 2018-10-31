# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Event
from .models import Organization

# Register your models here.
admin.site.register(Event)
admin.site.register(Organization)
