from django.shortcuts import render ,redirect
from .models import Post,Like,Comment, Job , JobRequest
from profiles.models import Profile , ConnectionRequest
from .forms import PostModelForm, CommentModelForm , JobModelForm
from django.views.generic import UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import  messages
from .forms import PostModelForm,JobModelForm,CommentModelForm
from django.shortcuts import get_object_or_404
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



def job_list_view(request):
    profile = Profile.objects.get(user=request.user)
    jobs = Job.objects.filter(author=profile)
    job_form = JobModelForm()
    job_added = False

    if 'submit_job_form' in request.POST:
        job_form = JobModelForm(request.POST, request.FILES)
        print(request.POST)
        if job_form.is_valid():
            instance = job_form.save(commit=False)
            instance.author = profile
            instance.save()
            instance.title = job_form.cleaned_data.get('title')
            instance.description = job_form.cleaned_data.get('description')
            instance.image = job_form.cleaned_data.get('image')
            instance.work_area = job_form.cleaned_data.get('work_area')
            instance.skills.add(*job_form.cleaned_data.get('skills'))
            instance.salary = job_form.cleaned_data.get('salary')
            job_form = JobModelForm()
            job_added = True

    context = {
        'profile': profile,
        'job_form': job_form,
        'job_added': job_added,
        'jobs': jobs,
    }
    return render(request, 'posts/joblist.html', context)


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
        pk = request.POST.get('job_id')
        user = request.user
        sender = Profile.objects.get(user=user)
        job = Job.objects.get(pk=pk)
        job_request = JobRequest.objects.create(sender=sender, value='Apply', job=job)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('job_list_view')


def approve_job_request(request):
    if request.method == 'POST':
        pk = request.POST.get('applicant_pk')
        print("applicant pk : " + pk)
        sender = Profile.objects.get(pk=pk)
        print("size of queryset : ", end="")
        print(len(sender))
        print("Request sender : ", end="")
        print(sender)
        job_request = get_object_or_404(JobRequest, sender=sender)
        job = job_request.job
        if job_request.status == 'apply':
            job_request.status = 'Approve'
            job_request.save()
            job.author.employees.add(sender.user)
            sender.clients.add(job.author.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:connection_request_view')



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



def job_detail_view(request, job_id):
    print(job_id)
    job = Job.objects.get(id=job_id)
    print(job)
    return render(request, 'posts/applicants.html', {'job': job})



