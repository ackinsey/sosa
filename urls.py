from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'experiment.views.home', name='home'),
    url(r'^create/', 'experiment.views.create', name='create'),
    url(r'^load/', 'experiment.views.load', name='load'),
    url(r'^admin/', include(admin.site.urls)),

)
