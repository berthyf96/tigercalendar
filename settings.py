import os

# ALLOWED_HOSTS = [
#     '.tigercalender.herokuapp.com',
# ]

#DEBUG = False

INSTALLED_APPS = [
    #...
    'myapp',
    #...
]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'events',
        'USER': 'bestteam',
        'PASSWORD': 'princeton',
        'HOST': 'localhost',
        'PORT': '3000',
    }
}