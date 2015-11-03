# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

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