from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404,JsonResponse
from django.views.generic import ListView, DetailView,View
from django.shortcuts import render
from billing.models import BillingProfile
from .models import *

class OrderListView(LoginRequiredMixin,ListView):
	def get_queryset(self):
		return Order.objects.by_request(self.request).not_created()

class OrderDetailView(LoginRequiredMixin,DetailView):
	template_name="orders/order_detail.html"
	def get_object(self):
		qs=Order.objects.all().get(order_id=self.kwargs.get('order_id'))
		return qs
class LibraryView(LoginRequiredMixin,ListView):
    template_name = 'orders/library.html'
    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)	


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET 
            print(data)
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404