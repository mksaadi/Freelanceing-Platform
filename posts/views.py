from django.shortcuts import render ,redirect
from .models import Post,Like,Comment, Job , JobRequest
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm , JobModelForm
from django.views.generic import UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib import  messages
# Create your views here.


def post_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.filter(author=profile)
    jobs = Job.objects.filter(author = profile)
    post_form = PostModelForm()
    comment_form = CommentModelForm()
    post_added = False
    comment_added = False
    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        print(request.POST)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_added = True
    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user  = profile
            comment.post =  Post.objects.get(id=request.POST.get('post_id'))
            comment.save()
            comment_form = CommentModelForm()
            comment_added = False

    context = {
        'qs': qs,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'comment_added': comment_added,
        'post_added': post_added,
        'jobs': jobs,
    }
    return render(request, 'posts/main.html', context)


def like_unlike_view(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = "Unlike"
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

    return redirect('posts:post_view')




class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)

        if not obj.author.user == self.request.user:
            messages.warning(self.request,'You are not authorized to delete this post.')
        return obj


class PostUpdateView(UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:post_view')

    def form_valid(self, form):
        profile = Profile.objects.get(user = self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None,"You are not authorized!")
            return super().form_invalid(form)



def send_request(request):
    if request.method == 'POST':
        pk = request.POST.get('job_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        job = Job.objects.get(pk=pk)
        job_request = JobRequest.objects.create(sender=sender, value='Apply',job = job)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:ProfileListView')




def find_jobs(request):
    profile = Profile.objects.get(user=request.user)
    all_jobs = Job.objects.all()
    related_jobs = []

    for job in all_jobs:
        if job.work_area == profile.work_area:
            related_jobs.append(job)


    print(related_jobs)
    context = {
        'profile': profile,
        'related_jobs': related_jobs,
        'all_jobs': all_jobs,
    }
    return render(request, 'profiles/jobs.html', context)


