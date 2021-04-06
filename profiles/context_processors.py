from .models import Profile
from .models import ConnectionRequest

def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        dp = profile.dp
        return {
            'dp': dp
        }
    return {}


def connection_request_received(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        qs_count = Profile.objects.get_all_request_received(profile).count()
        return {
            'request_no': qs_count,
        }
    return {}
