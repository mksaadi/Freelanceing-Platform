from django.shortcuts import  render
from. import views

def base_view(request):
    return render(request,'base.html')