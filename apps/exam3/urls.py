from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login),
    url(r'^dash$', views.dash),
    url(r'^logout$', views.logout),
    url(r'^addjob$', views.add),
    url(r'^submitjob$', views.addjob),
    url(r'^view/(?P<id>\d+)/$', views.view),
    url(r'^edit/(?P<id>\d+)/$', views.edit),
    url(r'^cancel/(?P<id>\d+)/$', views.cancel),
    url(r'^addingjob/(?P<id>\d+)/$', views.addingjob),
    url(r'^editlogic/(?P<id>\d+)/$', views.editlogic),
    url(r'^done/(?P<id>\d+)/$', views.done),

]