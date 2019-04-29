from django.conf.urls import include, patterns, url
from django.contrib import admin

from students.views.contact_admin import ContactView
from students.views.groups import (GroupCreateView, GroupDeleteView, GroupList,
                                   GroupUpdateView)
from students.views.journal import JournalView
from students.views.students import (StudentDeleteView, StudentList,
                                     StudentUpdateView)

from .settings import DEBUG, MEDIA_ROOT

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'studentsdb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),


                       # Students urls
                       url(r'^$',
                           StudentList.as_view(), name='home'),
                       # url(r'^$', 'students.views.students.students_list', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^students/add/$',
                           'students.views.students.students_add', name='students_add'),
                       url(r'^students/(?P<pk>\d+)/edit/$',
                           StudentUpdateView.as_view(), name='students_edit'),
                       url(r'^students/(?P<pk>\d+)/delete/$',
                           StudentDeleteView.as_view(), name='students_delete'),
                       # journal urls
                       url(r'^journal/(?P<pk>\d+)?/?$',
                           JournalView.as_view(), name='journal'),

                       # Group urls
                       url(r'^groups/$',
                           GroupList.as_view(), name='groups'),
                       url(r'^groups/add/$',
                           GroupCreateView.as_view(), name='groups_add'),
                       url(r'^groups/(?P<pk>\d+)/edit/$',
                           GroupUpdateView.as_view(), name='groups_edit'),
                       url(r'^groups/(?P<pk>\d+)/delete/$',
                           GroupDeleteView.as_view(), name='groups_delete'),

                       # Contact Admin Form
                       url(r'^contact-admin/$', ContactView.as_view(),
                           name='contact_admin'),

                       url(r'^admin/', include(admin.site.urls)),
                       )


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': MEDIA_ROOT}))
