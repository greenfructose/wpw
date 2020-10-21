from django.contrib import admin
from .models import Profile, FriendRequest, Tribe

admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Tribe)