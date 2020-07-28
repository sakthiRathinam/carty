from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import *
# Create your views here.
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,DetailView,View
from django.http import Http404
from cart.models import *
from analytics.mixins import * 
from analytics.models import *
from orders.models import ProductPurchase
class ProductFeaturedListView(ListView):
	template_name="products/list.html"

	def get_queryset(self,*args,**kwargs):
		request=self.request
		return Product.objects.all().featured()
class ProductSlugDetailView(ObjectViewedMixin,DetailView):
	queryset=Product.objects.all()
	template_name="products/detail.html"

	def get_context_data(self,*args,**kwargs):
		context=super(ProductSlugDetailView,self).get_context_data(*args,**kwargs)
		print(self.request)
		cart_obj,new_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_object(self,*args,**kwargs):
		request=self.request
		slug=self.kwargs.get('slug')

		try:
			instance=Product.objects.get(slug=slug,active=True)
		except Product.DoesNotExist:
			raise Http404("not found..")
		except Product.MultipleObjectsReturned:
			qs=Product.objects.filter(slug=slug,active=True)
			instance=qs.first()
		except:
			raise Http404('uhmmm')
		return instance
class UserProductHistoryView(ListView):
	template_name="analytics/objectviewed_list.html"

	def get_context_data(self,*args,**kwargs):
		context=super(UserProductHistoryView,self).get_context_data(*args,**kwargs)
		print(self.request)
		cart_obj,new_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context
	def get_queryset(self,*args,**kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product,model_queryset=False)
		return views


#class based view
class ProductListView(ListView):
	queryset=Product.objects.all()
	template_name="products/list.html"

	def get_context_data(self,*args,**kwargs):
		context=super(ProductListView,self).get_context_data(*args,**kwargs)
		print(self.request)
		cart_obj,new_obj=Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	#def get_context_data(self,*args,**kwargs):
		#context=super(ProductListView,self).get_context_data(*args,**kwargs)
		#print(context)
		#return context
class DetailListView(ObjectViewedMixin,DetailView):
	queryset=Product.objects.all()
	template_name="products/detail.html"

	def get_context_data(self,*args,**kwargs):
		context=super(DetailListView,self).get_context_data(*args,**kwargs)
		print(context)
		return context
	def get_object(self,*args,**kwargs):
		request=self.request
		pk=self.kwargs.get('pk')
		instance=Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404("Product doesnt exist")
		return instance
#function based view
def productView(request):
	qs=Product.objects.all()
	context={'object_list':qs}
	return render(request,'products/list.html',context)
def detailView(request,pk=None,*args,**kwargs):
	#instance=get_object_or_404(Product,pk=pk)
	instance=Product.objects.get_by_id(pk)
	#if qs.exists() and qs.count()!=0:
		#instance=qs.first()
	if instance==None:
		raise Http404("product doesnt exist")
	context={
		'object':instance
	}


	return render(request,'products/detail.html',context)
import os
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.conf import settings
class ProductDownloadView(View):
	def get(self,request,*args,**kwargs):
		slug = kwargs.get('slug')
		pk = kwargs.get('pk')
		download_qs = ProductFile.objects.filter(id=pk,product__slug=slug)
		if download_qs.count()!=1:
			raise Http404("Download not found")
		download_obj = download_qs.first()
		can_download = False
		user_ready=True
		if download_obj.user_required:
			if not request.user.is_authenticated:
				user_ready=False
		purchased_products=Product.objects.none()
		if download_obj.free:
			can_download=True
			user_ready=True
		else:
			purchased_products=ProductPurchase.objects.products_by_request(request)
			if download_obj.product in purchased_products:
				can_download=True
		if not download_obj or not user_ready:
			messages.error(request,"this item is not available for you")
			return redirect(download_obj.get_default_url())
		aws_filepath = download_obj.generate_download_url()
		print(aws_filepath)
		return HttpResponseRedirect(aws_filepath)
		"""file_root = settings.PROTECTED_ROOT
		filepath=download_obj.file.path
		final_filepath=os.path.join(file_root,filepath)
		with open(final_filepath,'rb') as f:
			wrapper = FileWrapper(f)
			mimetype = 'application/force-download'
			guessed_mimetype=guess_type(filepath)[0]
			if guessed_mimetype:
				mimetype = guessed_mimetype
			response = HttpResponse(wrapper,content_type=mimetype)
			response['Content-Disposition'] = f"attachment;filename={download_obj.name}"
			response["X-SendFile"] = str(download_obj.name)
			return response"""