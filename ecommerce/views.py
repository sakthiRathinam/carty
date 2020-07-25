from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.http import is_safe_url
from billing.models import *
from accounts.signals import *
def contactPage(request):
	contact=ContactForm(request.POST or None)
	context={
			"title":"contact",
			"content":"please tell valid resource",
			"form":contact,
	}

	if contact.is_valid():
		print(contact.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message":"Thank you for your submisson"})
	if contact.errors:
		errors=contact.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors,status=400,content_type='application/json')

	return render(request,'auth/contact.html',context)

def registerPage(request):
	form=UserForm()
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			user=form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,"Account was created successfully" + username)
			return redirect('login')
	context={'form':form}
	return render(request,'auth/register.html',context)
def loginPage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(request,username=username,password=password)
		next_post = request.POST.get('next')
		redirect_path =next_post
		print(redirect_path)
		if user is not None:
			print(request.POST)
			login(request,user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			try:
				del request.session['guest_email_id']
			except:
				pass
			if is_safe_url(redirect_path,request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("cart:home") 
		else:
			messages.info(request,'Username or password is incorrect')
	context={}
	return render(request,'auth/login.html',context)
User = get_user_model()
def logoutUser(request):
	logout(request)
	return redirect('products:list')
def guestView(request):
	if request.method =='POST':
		next_=request.POST.get('next')
		redirect_path=next_
		email=request.POST.get('email')
		new_guset_email=GuestProfile.objects.create(email=email)
		request.session['guest_email_id'] = new_guset_email.id
		if is_safe_url(redirect_path,request.get_host()):
			return redirect(redirect_path)
		else:
			return redirect('cart:home')
	return redirect('register')