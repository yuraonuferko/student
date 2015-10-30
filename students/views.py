# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# Views for Students
def students_list(request):
    students = (
    {'id': 1,
     'first_name': u'Корост',
     'last_name': u'Андрій',
     'ticket': 235,
     'image': 'img/me.jpeg'},
    {'id': 2,
     'first_name': u'Подоба',
     'last_name': u'Віталій',
     'ticket': 2123,
     'image': 'img/piv.png'},
    {'id': 3,
     'first_name': u'Онуферко',
     'last_name': u'Юрій',
     'ticket': 3333,
     'image': 'img/podoba3.jpg'},              
    )              
    return render(request, 'students/students_list.html',{'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)

# Views for Groups

def groups_list(request):
    leaders = (
    {'id': 1,
     'starosta': u'Корост Андрій ',
     'grupa': u'МТм-21'},
     
    {'id': 2,
     'starosta': u'Подоба Віталій',
     'grupa' :   u'МТм-22'},
    {'id': 3,
     'starosta': u'Онуферко Юрій',
     'grupa': u'МТм-23'},
)
    return render(request, 'students/groups_list.html',{'leaders':leaders})
    #return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
    return HttpResponse ('<h1>Group Add Form</h1')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s </h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s </h1>' % gid)