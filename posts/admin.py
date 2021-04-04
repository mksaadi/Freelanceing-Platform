from django.contrib import admin
from .models import Post, Like, Comment, Job , JobRequest, JobAppointment, Message


admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Job)
admin.site.register(JobRequest)
admin.site.register(JobAppointment)
admin.site.register(Message)
