from django.shortcuts import render,redirect
from .models import *
from orders.models import *
from billing.models import *
from addresses.forms import AddressForm
from addresses.models import *
from django.http import JsonResponse
from django.conf import settings
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_eFJDXUWedmd8J2GuJfkegNfG00YvUZ6p6v")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", "pk_test_b1TuhW27sl97xwjpUxro1Ceo00BxZwLYUD")
def cart_api_view(request):
	if request.is_ajax():


		cart_obj,new_obj=Cart.objects.new_or_get(request)
		products=[{"id":x.id,"url":x.get_absolute_url(),"name":x.title,"price":x.price} for x in cart_obj.products.all()]
		cart_data={"products":products,"subtotal":cart_obj.subtotal,"total":cart_obj.total}
		print(products)
		return JsonResponse(cart_data)
def cart_home(request):
	print(request.session)
	cart_obj,new_obj=Cart.objects.new_or_get(request)

	return render(request,'carts/home.html',{"cart":cart_obj})


def cart_update(request):
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj =Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("product is gone?..")
			return redirect("cart:home")
		cart_obj,new_obj=Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added=False
		else:
			cart_obj.products.add(product_obj)
			added=True
		request.session['cart_items']=cart_obj.products.count()
		if request.is_ajax():
			print("ajax request")
			json_data = {
				"added":added,
				"removed":not added,
				"cartItemCount":cart_obj.products.count(), 
			}
			return JsonResponse(json_data)

	return redirect("cart:home")

def checkoutProcess(request):
	cart_obj,cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	address_form = AddressForm()
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")
	billing_address_id = request.session.get("billing_address_id",None)
	shipping_address_id = request.session.get("shipping_address_id",None)
	shipping_address_required = not cart_obj.is_digital
	billing_profile,billing_profile_created = BillingProfile.objects.new_or_get(request)
	address_qs = None
	has_card=False
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj , order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)	
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session["shipping_address_id"]
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id:
			order_obj.save()
		has_card = billing_profile.has_card
		if request.method == "POST":
			"check that order is done"
			is_done = order_obj.check_done()
			did_charge,crg_msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				if not billing_profile.user:
					billing_profile.set_cards_inactive()
				return redirect("cart:success")
			else:
				print(crg_msg)
				return redirect("cart:checkout")
	context={
		"object":order_obj,
		"billing_profile":billing_profile,
		"address_form":address_form,
		"address_qs":address_qs,
		"has_card":has_card,
		"publish_key":STRIPE_PUB_KEY,
		"shipping_address_required":shipping_address_required
	}
	return render(request,"carts/checkout.html",context)


def checkout_success(request):
	return render(request,'carts/success.html',{})