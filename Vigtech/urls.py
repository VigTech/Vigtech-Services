from django.conf.urls import patterns, include, url
from django.contrib import admin
import principal.views
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'login'}, name='logout'),
    #url(r'^home/$' ,{'template_name':'home.html'}, name='home'),
    #url(r'^$' ,{'template_name':'home.html'}, name='home'),
    url(r'^', include('principal.urls')),
)
