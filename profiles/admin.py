from django.contrib import admin
from .models import Skill, Area, Profile ,ConnectionRequest, Rating
# Register your models here.
admin.site.register(Area)
admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(ConnectionRequest)
admin.site.register(Rating)
