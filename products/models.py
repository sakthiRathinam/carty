from django.db import models
import random
from django.conf import settings
from ecommerce.aws.download.utils import AWSDownload
from django.core.files.storage import FileSystemStorage
import os
from django.db.models.signals import pre_save,post_save
from ecommerce.utils import *
from django.db.models import Q
from django.urls import reverse
from ecommerce.aws.conf import ProtectedS3Storage
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
	is_digital = models.BooleanField(default=False)
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
	def get_downloads(self):
		qs=self.productfile_set.all()
		return qs
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
def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    #id_ = 0
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        id_ = qs.first().id + 1
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename #"path/to/filename.mp4"

class ProductFile(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	file = models.FileField(upload_to=upload_product_file_loc,storage=ProtectedS3Storage())
	free = models.BooleanField(default=False)
	user_required = models.BooleanField(default=False)
	name = models.CharField(max_length=120,null=True,blank=True)
	def __str__(self):
		return str(self.file.name)
	def get_default_url(self):
		return self.product.get_absolute_url()
	@property
	def display_name(self):
		og_name = get_filename(self.file.name)
		if self.name:
			return self.name
		return og_name
	def generate_download_url(self):
		bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
		region = getattr(settings, 'S3DIRECT_REGION')
		access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
		secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
		if not secret_key or not access_key or not bucket or not region:
			return "/product-not-found/"
		PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME', 'protected')
		path = "{base}/{file_path}".format(base=PROTECTED_DIR_NAME, file_path=str(self.file))
		aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
		file_url = aws_dl_object.generate_url(path,new_filename=self.display_name)#, new_filename='New awesome file')
		return file_url
	def get_download_url(self):
		return reverse("products:download",kwargs={"slug":self.product.slug,"pk":self.pk})