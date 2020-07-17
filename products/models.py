from django.db import models
import random
import os
from django.db.models.signals import pre_save,post_save
from ecommerce.utils import *
from django.db.models import Q
from django.urls import reverse
def get_filename_ext(filepath):
	baseName=os.path.basename(filepath)
	name,ext=os.path.splitext(baseName)
	return name,ext
def upload_image_path(instance,filename):
	print(instance)
	print(filename)
	newFilename=instance
	name,ext=get_filename_ext(filename)
	finalFilename=f'{newFilename}{ext}'
	return f"products/{newFilename}/{finalFilename}"
class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)
	def featured(self):
		return self.filter(featured=True,active=True)
	def search(self,query):
		lookups=(Q(title__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)|Q(tag__title__icontains=query))
		return self.filter(lookups).distinct()
class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model,using=self._db)
	def all(self):
		return self.get_queryset().active()
	def featured(self):
		return self.get_queryset().featured()
	def get_by_id(self,id):
		qs=self.get_queryset().filter(id=id)
		if qs.count()==1:
			return qs.first()
		return None
	def search(self,query):
		return self.get_queryset().active().search(query)

class Product(models.Model):
	title=models.CharField(max_length=100)
	slug=models.SlugField(blank=True,unique=True)
	description=models.TextField(null=True,blank=True)
	price=models.DecimalField(max_digits=10,decimal_places=2)
	image=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
	active=models.BooleanField(default=True)
	featured=models.BooleanField(default=False)
	objects=ProductManager()

	def __str__(self):
		return self.title
	def get_absolute_url(self):
		#return f"/productss1/{self.slug}/"
		return reverse("products:detail",kwargs={"slug":self.slug})
	@property
	def imageUrl(self):
		try:
			url=self.image.url
		except:
			url=""
		return url
def product_pre_save(sender,instance,*args,**kwargs):
	if not instance.slug:
		print(instance)
		instance.slug=unique_slug_generator(instance)
pre_save.connect(product_pre_save,sender=Product)

class ProductItems(models.Model):
	images=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
	@property
	def imagesUrl(self):
		try:
			url=self.images.url
		except:
			url=""
		return url
