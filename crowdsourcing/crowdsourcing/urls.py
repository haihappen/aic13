from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crowdsourcing.views.home', name='home'),
    # url(r'^crowdsourcing/', include('crowdsourcing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'web.views.tasks'),
    url(r'^tasks/$', 'web.views.tasks'),
    url(r'^tasks/(?P<task_id>\d+)/$', 'web.views.task_detail'),
    
    url(r'^answer_task/(?P<task_id>\d+)/$','web.views.answer_task'),
    #User related
    url(r'^signup/$','web.views.new_user'),
    url(r'^users/$','web.views.users'),
    
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^logout/$','web.views.destroy_session'),
    url(r'^accounts/logout/$','web.views.destroy_session'),
    url(r'^accounts/change_password/$','web.views.update_user'),
    url(r'^sessions/$','web.views.sessions'),
)
