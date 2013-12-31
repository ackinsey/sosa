from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'old.views.home', name='home'),

    # Uncomment the next line to enable the admin:
    url(r'^antiqueadmin/', include(admin.site.urls)),
)
