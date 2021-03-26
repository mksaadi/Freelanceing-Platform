from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, FreelancerRegistrationForm, ClientRegistrationForm, ProfileModelForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Area, ConnectionRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Model
from django.views.generic import ListView, UpdateView, DeleteView ,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from posts.forms import PostModelForm, JobModelForm, CommentModelForm
from posts.models import Job, Post, Comment


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'profiles/login.html', {'form': form})


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.filter(author=profile)
    connections = Profile.objects.get_all_friends_profile(request.user)
    all_posts = Post.objects.all()
    all_jobs = Job.objects.all()
    related_jobs = []
    connected_posts = []
    print("Connections of profile : ", profile)
    for post in all_posts:
        if post.author in connections:
            connected_posts.append(post)

    for job in all_jobs:
        if job.work_area == profile.work_area:
            related_jobs.append(job)


    post_form = PostModelForm()
    job_form = JobModelForm()
    comment_form = CommentModelForm()
    post_added = False
    job_added = False
    comment_added = False

    if 'submit_post_form' in request.POST:
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostModelForm()
            post_added = True

    if 'submit_job_form' in request.POST:
        job_form = JobModelForm(request.POST, request.FILES)
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
            post_form = JobModelForm()
            job_added = True



    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = profile
            comment.post = Post.objects.get(id=request.POST.get('post_id'))
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
        'connections': connections,
        'connected_posts': connected_posts,
        'job_form': job_form,
        'job_added': job_added,
        'related_jobs': related_jobs,

    }
    return render(request, 'profiles/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        print('Registering new user ')
        user_form = UserRegistrationForm(request.POST or None, request.FILES or None)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            print('Registration Successful!')
            return render(request, 'profiles/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'user_form': user_form})


def register_freelancer(request):
    if request.method == 'POST':
        print('Registering new user ')
        user_form = UserRegistrationForm(request.POST or None, request.FILES or None)
        profile_form = FreelancerRegistrationForm(request.POST or None, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.user_profile.is_freelancer = True
            new_user.user_profile.occupation = profile_form.cleaned_data.get('occupation')
            new_user.user_profile.education = profile_form.cleaned_data.get('education')
            new_user.user_profile.dp = profile_form.cleaned_data.get('dp')
            new_user.user_profile.cp = profile_form.cleaned_data.get('cp')
            new_user.user_profile.bio = profile_form.cleaned_data.get('bio')
            new_user.user_profile.phone_no = profile_form.cleaned_data.get('phone_no')
            new_user.user_profile.work_area = profile_form.cleaned_data.get('work_area')
            new_user.user_profile.skills.set(profile_form.cleaned_data.get('skills'))
            new_user.user_profile.pay_rate = profile_form.cleaned_data.get('pay_rate')
            new_user.user_profile.credit_card_no = profile_form.cleaned_data.get('credit_card_no')
            new_user.user_profile.save()
            return render(request, 'profiles/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = FreelancerRegistrationForm()

    return render(request, 'profiles/register_freelancer.html', {'user_form': user_form, 'profile_form': profile_form})


def register_client(request):
    if request.method == 'POST':
        print('Registering new user ')
        user_form = UserRegistrationForm(request.POST or None, request.FILES or None)
        profile_form = ClientRegistrationForm(request.POST or None, request.FILES or None)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.user_profile.is_client = True
            new_user.user_profile.occupation = profile_form.cleaned_data.get('occupation')
            new_user.user_profile.company = profile_form.cleaned_data.get('company')
            new_user.user_profile.dp = profile_form.cleaned_data.get('dp')
            new_user.user_profile.cp = profile_form.cleaned_data.get('cp')
            new_user.user_profile.bio = profile_form.cleaned_data.get('bio')
            new_user.user_profile.phone_no = profile_form.cleaned_data.get('phone_no')
            new_user.user_profile.phone_no = profile_form.cleaned_data.get('credit_card_no')

            new_user.user_profile.save()
            return render(request, 'profiles/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ClientRegistrationForm()
    return render(request, 'profiles/register_client.html', {'user_form': user_form, 'profile_form': profile_form, })




@login_required
def profile_view(request,user_id):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        "profile": profile,
        "form": form,
        "confirm": confirm,
    }
    return render(request, 'profiles/profile.html', context)



def load_skills(request):
    area_id = request.GET.get('area')
    print(area_id)
    skills = Skill.objects.filter(area_id=area_id)
    print(skills)
    return render(request, 'profiles/skills_dropdown_list_options.html', {'skills': skills})


def connection_request_view(request):
    profile = Profile.objects.get(user=request.user)
    print("Seeing connection requests of "+profile.user.username)
    connections_requests = ConnectionRequest.objects.filter(receiver=profile, status='sent')
    connections_requests = list(map(lambda x: x.sender, connections_requests))
    is_empty = False
    if len(connections_requests) == 0:
        is_empty = True
    print(connections_requests)
    context = {
        'profile': profile,
        'connections_requests': connections_requests,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.html', context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self):
        id = self.kwargs.get('id')
        print(id)
        profile = Profile.objects.get(id=id)
        print(profile)
        return profile

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        con_r = ConnectionRequest.objects.filter(sender=profile)
        con_s = ConnectionRequest.objects.filter(receiver=profile)
        con_receiver = []
        con_sender = []
        for item in con_r:
            con_receiver.append(item.receiver.user)
        for item in con_s:
            con_sender.append(item.sender.user)

        context["profile"] = profile
        context["con_receiver"] = con_receiver
        context["con_sender"] = con_sender
        context['posts'] = self.get_object().get_posts()
        len_post = len(self.get_object().get_posts())
        is_empty = False
        if len_post == 0:
            is_empty=True
        context['is_empty'] = is_empty
        return context






class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        con_r = ConnectionRequest.objects.filter(sender=profile)
        con_s = ConnectionRequest.objects.filter(receiver=profile)
        con_receiver = []
        con_sender = []
        for item in con_r:
            con_receiver.append(item.receiver.user)
        for item in con_s:
            con_sender.append(item.sender.user)

        context["profile"] = profile
        context["con_receiver"] = con_receiver
        context["con_sender"] = con_sender
        return context


def send_connection(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        connection = ConnectionRequest.objects.create(sender=sender,receiver=receiver,status='sent')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:ProfileListView')


def remove_connection(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        connection = ConnectionRequest.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver = sender))
        )
        connection.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:ProfileListView')


def approve_connection(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        receiver = Profile.objects.get(user=user)
        sender = Profile.objects.get(pk=pk)
        connection = get_object_or_404(ConnectionRequest,sender=sender, receiver=receiver)
        if connection.status == 'sent':
            connection.status = 'accepted'
            connection.save()
            receiver.connections.add(sender.user)
            sender.connections.add(receiver.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:ProfileListView')


def connection_list(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user

    connections = Profile.objects.get_all_friends_profile(user)
    print(connections)
    context= {
        'connections': connections,
        'profile': profile,
    }
    return render(request, 'profiles/connection_list.html', context)
