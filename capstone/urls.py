
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from babynamebook import views as book_views


urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'', include('babynamebook.urls')),
    url(r'^signup/$', book_views.signup, name='signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
