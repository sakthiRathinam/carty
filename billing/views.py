from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from .models import *
# Create your views here.
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_eFJDXUWedmd8J2GuJfkegNfG00YvUZ6p6v")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", "pk_test_b1TuhW27sl97xwjpUxro1Ceo00BxZwLYUD")
stripe.api_key = STRIPE_SECRET_KEY


def payment_method(request):
	billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
	if not billing_profile:
		return redirect("/cart")
	next_url=None
	next_=request.GET.get('q')
	print(request.GET)
	print(next_)
	if is_safe_url(next_,request.get_host()):
		next_url=next_
	return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY,"next_url":next_url})

def payment_method_createview(request):
	if request.method == "POST" and request.is_ajax():
		billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse({"message":"cannot find this user"},status=401)
		token = request.POST.get("token")
		if token is not None:
			new_card_obj = Card.objects.add_new(billing_profile,token)
			print(new_card_obj)
		return JsonResponse({"message":"success your card is add"})
	return HttpResponse("error",status=401)