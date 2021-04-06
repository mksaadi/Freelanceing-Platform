from django.db import models
from profiles.models import Profile, Skill, Area
from posts.models import Job, JobRequest,JobAppointment
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete



# Create your models here.

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_receiver')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
