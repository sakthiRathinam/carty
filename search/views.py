from django.shortcuts import render
from django.views.generic import ListView
from products.models import *

class SearchProductView(ListView):
	template_name="search/view.html"

	def get_context_data(self,*args,**kwargs):
		context=super(SearchProductView,self).get_context_data(*args,**kwargs)
		query=self.request.GET.get('q')
		context['query']=query
		print(context)
		return context
	def get_queryset(self,*args,**kwargs):
		request=self.request
		method_dict=request.GET
		query=method_dict.get('q',None)
		print(query)

		if query is not None:
			return Product.objects.search(query)
		return Product.objects.all() 
def searchView(request):
	object_list=Product.objects.all()
	if request.method=='GET':
		print(request.GET)
		m=request.GET.get('q',None)
		print(m)
		if m is not None:
			object_list=Product.objects.search(m)
	context={'object_list':object_list,'query':m}
	return render(request,'search/view.html',context)