from django.contrib import admin

from .models import Membership, Tribes, User

admin.site.register(User)
admin.site.register(Tribes)
admin.site.register(Membership)
