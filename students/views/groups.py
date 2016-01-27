# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from ..models.groups import Group
# Views for Groups

def groups_list(request):
    leaders = Group.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by=='':
        leaders=leaders.order_by('title')
        all_range_groups=Group.objects.values_list('id', flat=True).order_by('title')
    if order_by in ('title', 'leader','id'):
        leaders = leaders.order_by(order_by)
        all_range_groups=Group.objects.values_list('id', flat=True).order_by(order_by)
        
        #for i in range(1,len(all_range_students)+1):value+=value[i]
        if request.GET.get('reverse', '') == '1':
            leaders = leaders.reverse
            p=Group.objects.values_list('id', flat=True).order_by(order_by)
            all_range_groups=p.reverse()
    
    try:
        page = int(request.GET.get('page'))
    except: 
        page=1
        
    
    
    def group1(all_range_groups, count):
          # """ Группировка элементов последовательности по count элементов """
        return [all_range_groups[i:i + count] for i in range(0, len(all_range_groups), count)]
    page_all=group1(all_range_groups,2)
    storinka=range(1,len(page_all) +1)
    start_page=page_all.index(page_all[0])+1
    end_page=len(page_all)
    b=0
    value={}
    for i in storinka:
        value.update({i:b})
        b+=3
    for i,j in zip(storinka,page_all):
        if i==page:
            leaders=[Group.objects.get(id=x) for x in j ]
            if i in value.keys():
                value=value.get(i)
    return render(request, 'students/groups_list.html',{'leaders':leaders,'page':page,'start_page':start_page,'end_page':end_page,
                                                        'storinka':storinka,'value':value,'order_by':order_by})

    #return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
    return HttpResponse ('<h1>Group Add Form</h1')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s </h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s </h1>' % gid)