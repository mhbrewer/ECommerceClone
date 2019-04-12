##### E-Commerce Website Clone
##### Mason Brewer
##### March 16th, 2019

from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.loginPage),
    url(r'^login$', views.loginPage),
    url(r'^login/process$', views.loginProcess),
    url(r'^login/?P<pHash>\w+$', views.paramLogin),
    url(r'^orders$', views.ordersPage),
    url(r'^products$', views.productsPage),
    url(r'^product/delete$', views.productDelete),
    url(r'^order/(?P<orderID>[0-9]+)$', views.orderViewPage),
    url(r'^changestatus$', views.changeStatus),
    url(r'^product/new$', views.productNewPage),
    url(r'^product/new/process$', views.productNewProcess),
    url(r'^product/edit$', views.productEditPage),
    url(r'^product/edit/process$', views.productEditProcess),
    url(r'^category/new/process$', views.categoryNewProcess),
    url(r'^admins', views.adminsPage),
    url(r'^admin/new$', views.adminNewPage),
    url(r'^admin/new/process$', views.adminNewProcess),
    url(r'^admum$', views.admumsTheWord),
    url(r'^logout$', views.logout),
]