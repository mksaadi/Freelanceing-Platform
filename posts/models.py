from django.db import models
from profiles.models import Profile, Skill, Area
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete




class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    def all_comments(self):
        return self.comment_set.all()


    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def get_username(self):
        return self.user.user.username

    def get_user_dp(self):
        return self.user.dp





class Like(models.Model):
    LIKE_CHOICES = [
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    ]
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


class Job(models.Model):
    title = models.CharField(max_length=30, null=True)
    description = models.TextField(max_length=50)
    image = models.ImageField(upload_to='posts', blank=True)
    applicants = models.ManyToManyField(Profile, blank=True, related_name='job_applicants')

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='jobs')
    work_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='job_work_area', null=True)
    skills = models.ManyToManyField(Skill, null=True, related_name='job_skills')
    available = models.BooleanField(default=True)
    salary = models.PositiveIntegerField(default=0)

    def get_skills(self):
        return self.skills.all()

    def get_applicants(self):
        return self.applicants.all()

    def get_applicants_no(self):
        return self.applicants.all().count()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-created',)


class JobRequest(models.Model):
    APPLY_CHOICES = [
        ('applied', 'applied'),
        ('appointed', 'appointed'),
    ]
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='job_req_sender', default=None)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='job_req_receiver', default=None)
    status = models.CharField(choices=APPLY_CHOICES, max_length=10, default='applied')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job}-{self.status}"


@receiver(post_save, sender=JobRequest)
def post_save_add_applicants(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    job_ = instance.job
    if instance.status == 'applied':
        job_.applicants.add(sender_)
        job_.save()
    elif instance.status == 'appointed':
        receiver_.employees.add(sender_.user)
        sender_.clients.add(receiver_.user)
        job_.is_available = False
        job_.applicants.remove(sender_)
        job_.save()
        sender_.save()
        receiver_.save()



class JobAppointment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    content = models.CharField(max_length=20)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job}-{self.content[:10]}"




