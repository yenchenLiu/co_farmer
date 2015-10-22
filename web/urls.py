"""co_farmer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$',views.farmer_Account),
    url(r'^logout$',views.logout),
    url(r'^All_Farmer$',views.ALL_Farmer),
    url(r'^about/(?P<userId>\d{0,50})/$',views.about),
    url(r'^story/(?P<userId>\d{0,50})/$',views.story),
    url(r'^farmer_introduction/(?P<userId>\d{0,50})/$',views.farmer_introduction),
    url(r'^product_introduction/(?P<productId>\d{0,50})/$',views.product_introduction),
    
]
