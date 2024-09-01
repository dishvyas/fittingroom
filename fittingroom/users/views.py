from django.shortcuts import render, redirect
from django.db.models import Max
from django.template import loader
from django.views.generic.edit import UpdateView, CreateView
from users.forms import UserCreateForm
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserCreateForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def image_view(request):
    return render(request, 'fittingroom/image.html')

def index(request):
    return render(request,"fittingroom/home.html")


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "registration/register.html"

    def get_success_url(self):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password1'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('image')  
        return reverse('register')