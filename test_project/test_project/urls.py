from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import autocomplete_light
autocomplete_light.autodiscover()

import views

urlpatterns = patterns('',
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomeView.as_view(), name='home'),
)
