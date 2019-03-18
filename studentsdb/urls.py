from django.conf.urls import include, patterns, url
from django.contrib import admin

from students.views.contact_admin import ContactView
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
                           'students.views.groups.groups_list', name='groups'),
                       url(r'^groups/add/$',
                           'students.views.groups.groups_add', name='groups_add'),
                       url(r'^groups/(?P<gid>\d+)/edit/$',
                           'students.views.groups.groups_edit', name='groups_edit'),
                       url(r'^groups/(?P<gid>\d+)/delete/$',
                           'students.views.groups.groups_delete', name='groups_delete'),

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
