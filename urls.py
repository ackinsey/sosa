from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'experiment.views.home', name='home'),
    # url(r'^sosa/', include('sosa.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
