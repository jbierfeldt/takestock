from django.conf.urls import include, patterns, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns(
    '',
    url(r'^$', 'takestock.views.index'),
    url(r'^clubs/$', 'takestock.views.club_general', name='club_general'),
    url(r'^clubs/(?P<club_id>\d+)/$', 'takestock.views.club_detail',
        name='club_detail'),               
    url(r'^clubs/(?P<club_id>\d+)/pdf/$', 'takestock.views.club_detail_pdf',
        name='club_detail_pdf'),               
)
