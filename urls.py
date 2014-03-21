from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'experiment.views.home', name='home'),
    url(r'^run/', 'experiment.views.run', name='run'),    
    url(r'^create/', 'experiment.views.create', name='create'),
    url(r'^load/', 'experiment.views.load', name='load'),
    url(r'^view_stimuli/', 'experiment.views.view_stimuli', name='view_stimuli'),
    url(r'^finish/', 'experiment.views.finish', name='finish'),
    url(r'^about/', 'experiment.views.about', name='about'),
    url(r'^view/', 'experiment.views.view_results', name='view results'),
    url(r'^admin/', include(admin.site.urls)),



)
