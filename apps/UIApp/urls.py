##### E-Commerce Website Clone
##### Mason Brewer
##### March 16th, 2019

from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.homePage),
    url(r'^login$', views.loginPage),
    url(r'^login/process$', views.loginProcess),
    url(r'^registration/process$', views.regProcess),
    url(r'^category/(?P<catId>\w+)$', views.catPage),
    url(r'^item/(?P<itemID>[0-9]+)$', views.itemPage),
    url(r'^item/add$', views.addToCart),
    url(r'^checkout$', views.checkoutPage),
    url(r'^checkout/process$', views.checkoutProcess),
    url(r'^logout$', views.logout),
    url(r'^mum$', views.mumsTheWord),
]