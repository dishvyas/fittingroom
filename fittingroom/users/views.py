from django.shortcuts import render
from django.shortcuts import render_to_response
from django.db.models import Max
from django.template import loader
from django.views.generic.edit import UpdateView, CreateView
from users.forms import UserCreateForm
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Users
from .forms import UserCreateForm


def index(request):
    return render(request,"home.html")



class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "fittingroom/login.html"

    def get_success_url(self):
        user = authenticate(username=self.request.POST['username'], password=self.request.POST['password1'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return render(self,"index (1).html")
        return reverse('register')