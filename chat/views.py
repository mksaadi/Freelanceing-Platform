from django.shortcuts import render ,redirect,reverse
from .models import Message
from profiles.models import Profile, ConnectionRequest, Rating
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def chatroom(request, user_id):
    profile = Profile.objects.get(user=request.user)
    print(profile)
    other_user = get_object_or_404(Profile, id=user_id)
    print(other_user)
    messages = Message.objects.filter(
        Q(receiver=other_user, sender=profile) | Q(receiver=profile, sender=other_user)
    )
    context = {
        'profile': profile,
        'messages': messages,
        'other_user': other_user,
    }
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=profile))
    return render(request, "chat/chatroom.html", context)


@login_required
def ajax_load_messages(request, user_id):
    other_user = get_object_or_404(Profile, id=user_id)
    print(other_user)
    profile = Profile.objects.get(user=request.user)
    print(profile)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=profile, sender=other_user)
    )
    message_list = [{
        "sender": message.sender.user.username,
        "message": message.message,
        "sent": message.sender == profile
    } for message in messages]
    messages.update(seen=True)

    if request.method == "POST":
        message = json.loads(request.body)
        m = Message.objects.create(receiver=other_user, sender=profile, message=message)
        message_list.append({
            "sender": profile.user.username,
            "message": m.message,
            "sent": True,
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)