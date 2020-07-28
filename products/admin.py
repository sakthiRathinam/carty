from django.contrib import admin
from .models import *
# Register your models here.
class ProductFileInline(admin.TabularInline):
	model = ProductFile
	extra = 1

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug', 'is_digital']
	inlines =[ProductFileInline]
	class Meta:
		model = Product
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductItems)