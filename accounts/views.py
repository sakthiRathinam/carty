from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView,UpdateView
from django.urls import reverse

from .forms import *

class AccountHomeView(LoginRequiredMixin,DetailView):
	template_name = 'accounts/home.html'
	def get_object(self):
		return self.request.user
class UserDetailUpdateView(LoginRequiredMixin,UpdateView):
	form_class=UserDetailChangeForm
	template_name='accounts/detailUpdate.html'
	def get_object(self):
		return self.request.user
	def get_context_data(self,*args,**kwargs):
		context =super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
		context['title'] = 'change your Account Details'
		return context
	def get_success_url(self):
		return reverse("accounts:home")
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    redirect_path = next_
    if form.is_valid():
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("cart:home")
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request, "accounts/login.html", context)


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request, "auth/register.html", context)