from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload_tree/$', views.upload_tree, name='upload_tree'),
    url(r'^progress/$', views.progress, name='progress'),
]
