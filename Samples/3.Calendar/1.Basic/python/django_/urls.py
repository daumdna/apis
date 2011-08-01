from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

prefix = 'tutorial_python/calender/django/'
STATIC_ROOT = '/home/mademin/service/wwwroot/tutorial_python/calender/django_/static/'

urlpatterns = patterns('',
    url(prefix + 'oauth/main','django_.oauth_.views.index'),
    url(prefix + 'oauth/request_token','django_.oauth_.views.request_token'),
    url(prefix + 'oauth/callback','django_.oauth_.views.callback'),
    url(prefix + 'oauth/access_resource','django_.oauth_.views.access_resource'),
    url(prefix + r'calender/main/(?P<search_date>\d+-\d+)$','django_.calender.views.index'),
    url(prefix + 'calender/main/create_event$','django_.calender.views.create_event'),
    url(prefix + 'calender/main/view_event$','django_.calender.views.view_event'),
    url(prefix + 'calender/main/delete_event$','django_.calender.views.delete_event'),
    url(prefix + 'calender/main/$','django_.calender.views.index'),
    url(prefix + 'main','django_.calender.views.index'),
    url(prefix + 'static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': STATIC_ROOT}) 

    # Examples:
    # url(r'^$', 'django_.views.home', name='home'),
    # url(r'^django_/', include('django_.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
