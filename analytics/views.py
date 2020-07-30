from django.shortcuts import render
from django.utils import timezone
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,Http404,JsonResponse
from django.db.models import Count,Sum,Avg
from django.views.generic import TemplateView,View
from orders.models import Order
class SalesAjaxView(View):
	def get(self,request,*args,**kwargs):
		data={}
		print(request.user)
		if request.user.is_authenticated:
			qs = Order.objects.all().by_weeks_range(weeks_ago=5,number_of_weeks=5)
			if request.GET.get('type')=='week':
				days=7
				start_date = timezone.now().today() - datetime.timedelta(days=days-1)
				datetime_list =[]
				labels = []
				salesItems=[]
				for x in range(0,days):
					new_time = start_date + datetime.timedelta(days=x)
					datetime_list.append(new_time)
					labels.append(new_time.strftime("%a"))
					new_qs=qs.filter(updated__day=new_time.day,updated__month=new_time.month)
					day_total = new_qs.totals_data()['total__sum'] or 0
					salesItems.append(day_total)
				data['labels']=labels
				data['data']=salesItems			
			if request.GET.get('type')=='4weeks':
				data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
				current = 5
				data['data'] = []
				for i in range(0, 5):
					new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
					sales_total = new_qs.totals_data()['total__sum'] or 0
					data['data'].append(sales_total)
					current -= 1
				print(data['data'])
		return JsonResponse(data)

class SalesView(LoginRequiredMixin,TemplateView):
	template_name = 'analytics/sales.html'

	def dispatch(self,*args,**kwargs):
		user = self.request.user
		if not user.is_authenticated:
			raise Http404
		return super(SalesView,self).dispatch(*args,**kwargs)

	def get_context_data(self,*args,**kwargs):
		context = super(SalesView,self).get_context_data(*args,**kwargs)
		qs = Order.objects.all().by_weeks_range(weeks_ago=10,number_of_weeks=10)
		#context['orders'] = qs
		#context['recent_orders'] = qs.not_refunded()[:5]
		#context['recent_orders_total'] = context['recent_orders'].totals_data()
		#context['cart_total']=context['recent_orders'].cart_data()
		# context['recent_cart_data'] = context['recent_orders'].aggregate(
        #                                 Avg("cart__products__price"), 
        #                                 Count("cart__products")
        #                             )
        # qs = Order.objects.all().aggregate(Sum("total"), Avg("total"), Avg("cart__products__price"), Count("cart__products"))
        # ann = qs.annotate(product_avg=Avg('cart__products__price'), product_total = Sum('cart__products__price'), product__count = Count('cart__products'))	
		#context['shipping_orders'] = qs.not_refunded().by_status(status="shipped")[:5]
		#context['shipping_orders_total']=context['shipping_orders'].totals_data()		
		#context['paid_orders'] = qs.not_refunded().by_status(status="paid")[:5]
		#context['paid_orders_total']=context['paid_orders'].totals_data()
		context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
		context['this_week'] = qs.by_weeks_range(weeks_ago=1,number_of_weeks=1).get_sales_breakdown()
		context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=2).get_sales_breakdown()
		print(context['last_four_weeks'])
		return context