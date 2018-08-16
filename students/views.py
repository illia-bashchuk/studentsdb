# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def students_list(request):
	students = (
	{'id': 1,
	'first_name': u'Віталій',
	'last_name': u'Подоба',
	'ticket': 235,
	'image': 'img/me.jpeg'},
	{'id': 2,
	'first_name': u'Корост',
	'last_name': u'Андрій',
	'ticket': 2123,
    'image': 'img/piv.png'},
	{'id': 3,
	'first_name': u'Притула',
	'last_name': u'Тарас',
	'ticket': 2123,
    'image': 'img/piv.png'},
	)
	return render(request, 'students/students_list.html', {})



# Views for Students
def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

def students_list(request):
	return render(request, 'students/students_list.html', {})

    #Views for Groups
def groups_list(request):
	return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
