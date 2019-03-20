# -*- coding: utf-8 -*-
from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, ListView, UpdateView

from ..models.groups import Group

from ..util import get_current_group, paginate

# Views for Groups


class GroupList(ListView):
    model = Group
    context_object_name = 'groups1'
    template_name = 'students/group.html'
    paginate_by = 3
    page_kwarg = 'page'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        qs = super(GroupList, self).get_queryset()
        #print current_group
        
        if current_group:
            return qs.filter(pk=current_group.id)
        else:
            # otherwise show all groups
            return qs.all()


"""def groups_list(request):
    groups = (
        {'id': 1,
         'group_name': u'МтМ-21',
         'leader_name': u'Ячменев Олег'},
        {'id': 2,
         'group_name': u'МтМ-22',
         'leader_name': u'Віталій Подоба'},
        {'id': 3,
         'group_name': u'МтМ-23',
         'leader_name': u'Іванов Андрій'},
    )
    return render(request, 'students/group.html', {'groups': groups})
#	return HttpResponse('<h1>Groups Listing</h1>')"""


def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
