from django.db import models
from profiles.models import Profile, Skill, Area


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

    def __str__(self):
        return str(self.description[:20])

    class Meta:
        ordering = ('-created',)


class Apply(models.Model):
    APPLY_CHOICES = [
        ('Withdraw', 'Withdraw'),
        ('Apply', 'Apply'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.CharField(choices=APPLY_CHOICES, max_length=8)
    job = models.ForeignKey(Post, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.job}-{self.value}"
