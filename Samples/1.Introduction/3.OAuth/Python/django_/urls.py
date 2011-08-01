from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
prefix = 'tutorial_python/oauth/django/'

urlpatterns = patterns('',
    # Examples:
    url(prefix + r'oauth/main',r'django_.oauth_.views.index'),
    url(prefix + r'oauth/request_token',r'django_.oauth_.views.request_token'),
    url(prefix + r'oauth/callback',r'django_.oauth_.views.callback'),
    url(prefix + r'oauth/access_resource',r'django_.oauth_.views.access_resource')


    # url(r'^$', 'django_.views.home', name='home'),
    # url(r'^django_/', include('django_.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
