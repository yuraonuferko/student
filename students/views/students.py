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