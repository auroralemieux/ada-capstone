from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^get_tree_instructions/$', views.get_tree_instructions, name='get_tree_instructions'),
    url(r'^upload_tree/$', views.upload_tree, name='upload_tree'),
    url(r'^progress/$', views.progress, name='progress'),
    url(r'^correlate/$', views.correlate, name='correlate'),
    url(r'^account/$', views.account, name='account'),
    url(r'^book/(?P<pk>\d+)/$', views.book, name='book'),

]
