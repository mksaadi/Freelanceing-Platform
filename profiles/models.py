from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import reverse
from django.core.validators import MinValueValidator, MaxValueValidator



class Area(models.Model):
    area = models.CharField(max_length=20)
    def __str__(self):
        return str(self.area)


class Skill(models.Model):
    skill = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.skill)


class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = ConnectionRequest.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        accepted = []
        for con in qs:
            if con.status == 'accepted':
                accepted.append(con.receiver)
                accepted.append(con.sender)

        print(accepted)
        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_friends_profile(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = ConnectionRequest.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)
        accepted = []
        for con in qs:
            if con.status == 'accepted':
                accepted.append(con.receiver)
                accepted.append(con.sender)

        print(accepted)
        available = [profile for profile in profiles if profile  in accepted]
        print(available)
        return available

    def get_all_request_received(self,receiver):
        qs = ConnectionRequest.objects.filter(receiver=receiver, status='sent')
        return qs


    def get_all_profiles(self,me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_all_raters_profile(self, sender):
        profile = Profile.objects.get(user = sender)
        raters_profiles = []
        ratings = Rating.objects.filter(receiver=profile)
        for rating in ratings:
            raters_profiles.append(rating.sender)

        print(raters_profiles)
        return raters_profiles




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    is_client = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    bio = models.TextField(default='no bio...', max_length=300)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    dp = models.ImageField(default='ddp.png', upload_to='dps/')
    cp = models.ImageField(default='dcp.png', upload_to='cps/')
    occupation = models.CharField(max_length=20, blank=True)
    education = models.CharField(max_length=20, blank=True)
    credit_card_no = models.CharField(max_length=25, blank=True)
    phone_no = models.CharField(max_length=20, blank=True)
    connections = models.ManyToManyField(User, blank=True, related_name='connected_users')
    # for freelancers
    work_area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True,related_name='skilled_freelancers')
    clients = models.ManyToManyField(User, blank=True, related_name='experienced_freelancer')
    pay_rate = models.PositiveIntegerField(default=0, blank=True)
    earning = models.PositiveIntegerField(default=0, blank=True)
    website = models.URLField(max_length=20, null=True, blank=True)
    # for client
    employees = models.ManyToManyField(User, blank=True,related_name='experienced_client')
    spending = models.PositiveIntegerField(default=0, blank=True)
    company = models.CharField(max_length=20,blank=True)
    objects = ProfileManager()

    def get_absolute_url(self):
        return reverse("profiles:ProfileDetailView", kwargs={"id": self.id})


    def get_all_raters_count(self):
        return self.rating_sender_set.all().count()


    def get_employees(self):
        return self.employees.all()

    def get_employee_no(self):
        return self.employees.all().count()

    def get_clients(self):
        return self.clients.all()

    def get_client_no(self):
        return self.clients.all().count()

    def get_skills(self):
        return list(self.skills.all())

    def get_number_of_skills(self):
        return self.skills.all().count()


    def get_posts_no(self):
        return self.posts.all().count()

    def get_posts(self):
        return self.posts.all()

    def get_connections(self):
        return self.connections.all()

    def get_number_of_connections(self):
        return self.connections.all().count()


    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value =='Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
             total_liked += item.liked.all().count()
        return total_liked


    def __str__(self):
        return f'Profile for user {self.user.username}--{self.created.strftime("%d-%m-%Y")}'



class Rating(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rating_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rating_receiver')
    score = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(default=None, max_length=100)

    def __str__(self):
        return str(self.pk)





@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created,**kwargs):
    print('sender', sender)
    print('instance', instance)
    if created:
        Profile.objects.get_or_create(user=instance)



# connection class
class ConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ('sent', 'sent'),
        ('accepted', 'accepted'),
    ]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


@receiver(post_save, sender=ConnectionRequest)
def post_save_add_connection(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.connections.add(receiver_.user)
        receiver_.connections.add(sender_.user)
        sender_.save()
        receiver_.save()



@receiver(pre_delete,sender=ConnectionRequest)
def pre_delete_remove_connection(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.connections.remove(receiver.user)
    receiver.connections.remove(sender.user)
    sender.save()
    receiver.save()


