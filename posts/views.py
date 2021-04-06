from django.shortcuts import render ,redirect,reverse
from .models import Post,Like,Comment, Job , JobRequest,Message
from profiles.models import Profile , ConnectionRequest, Rating
from .forms import PostModelForm, CommentModelForm , JobModelForm , AppointmentForm
from django.views.generic import UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import  messages
from .forms import PostModelForm, JobModelForm, CommentModelForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import humanize
# Create your views here.
from django.http import JsonResponse

def post_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.filter(author=profile)
    jobs = Job.objects.filter(author = profile,available = True)
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
        post_obj = Post.objects.get(id=post_id)
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



def send_job_request(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        req_sender = Profile.objects.get(user=request.user)
        req_job = Job.objects.get(id=job_id)
        req_receiver = req_job.author
        new_job_request = JobRequest.objects.create(sender=req_sender, receiver=req_receiver, job=req_job, status = 'applied')
        new_job_request.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('connection_request_view')





def approve_job_request(request):
    if request.method == 'POST':
        print("Approve method called.")
        print('*********')
        jpk = request.POST.get('request_pk')
        job_request = get_object_or_404(JobRequest, pk=jpk)
        print("******")
        print(job_request)
        sender_ = job_request.sender
        receiver_ = job_request.receiver
        job = job_request.job
        if job_request.status == 'applied':
            job.status = 'appointed'
            job.winner = sender_
            job_author = job_request.job.author
            job_author.employees.add(sender_.user)
            sender_.clients.add(receiver_.user)
            job.applicants.remove(sender_)
            job.available = False
            receiver_.save()
            sender_.save()
            job_request.save()
            job.save()
            job_request.delete()
            return  redirect('connection_request_view')
    return redirect('connection_request_view')



def find_jobs(request):
    profile = Profile.objects.get(user=request.user)
    all_jobs = Job.objects.filter(available=True)
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


def employee_list(request):
    profile = Profile.objects.get(user=request.user)
    employees = profile.employees.all()
    employee_profiles = []

    for employee in employees:
        emp_profile = Profile.objects.get(user=employee)
        employee_profiles.append(emp_profile)
    print(employee_profiles)

    context = {
        'profile': profile,
        'employee_profiles': employee_profiles,
    }
    return render(request, 'posts/employees.html', context)



def workspaces(request):

    profile = Profile.objects.get(user=request.user)
    if profile.is_freelancer:
        jobs = Job.objects.filter(winner=profile)
    else:
        jobs = Job.objects.filter(author=profile)

    context = {
        'jobs': jobs,
        'profile':profile,
    }
    return render(request,'posts/workspaces.html',context)

# message view


