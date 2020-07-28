from django.contrib import admin
from django.urls import path
from .views import *
app_name='products'
app_name='search'
urlpatterns = [
   path('',ProductListView.as_view(),name="list"),
   path('detail/<int:pk>/',DetailListView.as_view()),
   path('detail1/<int:pk>/',detailView),
   path('products1/',productView),
   path('productss/',ProductFeaturedListView.as_view()),
   path('productss1/<slug:slug>/',ProductSlugDetailView.as_view(),name="detail"),
   path('<slug:slug>/<int:pk>',ProductDownloadView.as_view(),name="download"),
]

app_name='products'