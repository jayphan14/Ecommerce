from django.contrib import admin
from django.contrib.auth.models import User
from .models import Listing, Bid, Comment

# Register your models here.

admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
