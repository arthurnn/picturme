from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='home'),
    url(r'^detail/$', direct_to_template, {'template': 'details.html'}, name='detail'),
    url(r'^loading/$', direct_to_template, {'template': 'loading.html'}, name='loading'),

    url(r'^admin/', include(admin.site.urls)),
)
