from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from .forms import RegistrationForm,LoginForm
from .models import User
from django.urls import reverse

from django.http.response import StreamingHttpResponse
from .camera import gen_frames
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def logout_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(uid=request.user.uid)
        user.face_auth = False
        user.save()
        logout(request)
    return redirect('/')


def home(request):
    return render(request,'index.html')

class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)

        return success_url

# def gen(camera):
# 	while True:
# 		frame = camera.get_frame()
# 		yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# def two_factor(request,user):
#     return render(request,'feed.html')

def welcome(request,user):
    user = User.objects.get(username = user)
    if user.face_auth:
        user.face_auth = False
        user.save()
        login(request,user)
    return render(request,'welcome.html')

def facecam_feed(request,user):
    user = User.objects.get(username=user)
    stream = gen_frames(request,user)
    return StreamingHttpResponse(stream,content_type='multipart/x-mixed-replace; boundary=frame')

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # login(request,user)
                return render(request,'feed.html',{'user':user.username})
            else:
                return render(request,'registration/login.html',{'form':form,'error':'Invalid Credentials'})
        else:
            return render(request,'registration/login.html',{'form':form})

    form = LoginForm()
    return render(request,'registration/login.html',{'form':form})

def checkAuth(request,user):
    val = User.objects.get(username=user)
    return JsonResponse({'auth':val.face_auth})
