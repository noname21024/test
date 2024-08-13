from django.contrib import admin
from users.models import  Messages, Profile

admin.site.register(Profile)
admin.site.register(Messages)