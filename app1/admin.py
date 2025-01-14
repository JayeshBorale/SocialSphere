from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(User_Posts)

admin.site.register(Comment)
admin.site.register(notification)
