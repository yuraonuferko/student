# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from django.template import Context, Template 

# Create your views here.

# Views for Students
def students_list(request):
    students = Student.objects.all()          
    #number_students=range(1,len(students)+1)
    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by=='':
        students=students.order_by('last_name')
        all_range_students=Student.objects.values_list('id', flat=True).order_by('last_name')
    if order_by in ('last_name', 'first_name', 'ticket','id'):
        students = students.order_by(order_by)
        all_range_students=Student.objects.values_list('id', flat=True).order_by(order_by)
        
        #for i in range(1,len(all_range_students)+1):value+=value[i]
        if request.GET.get('reverse', '') == '1':
            students = students.reverse
            p=Student.objects.values_list('id', flat=True).order_by(order_by)
            all_range_students=p.reverse()
    
    try:
        page = int(request.GET.get('page'))
    except: 
        page = 1
    #except EmptyPage:
     #   page=end_page
    # потрібно обчислити змінну all_range_students відповідно до сортування. Передати список id у відсортованому списку
    
    def group(all_range_students, count):
          # """ Группировка элементов последовательности по count элементов """
        return [all_range_students[i:i + count] for i in range(0, len(all_range_students), count)]
    page_all=group(all_range_students,3)
    #Список сторінок по їх номерах
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
            students=[Student.objects.get(id=x) for x in j ]
            if i in value.keys():
                value=value.get(i)
                   
    #students=student.objects.get(id=1)
    #try:
            #students = paginator.page(page)
    #except PageNotAnInteger:
               # If page is not an integer, deliver first page.
            #students = paginator.page(1)
    #except EmptyPage:
                # If page is out of range (e.g. 9999), deliver
                # last page of results.
            #students = paginator.page(paginator.num_pages)
    return render(request, 'students/students_list.html',{'students': students,'start_page':start_page,
                                                          'end_page':end_page,'storinka':storinka,'page':page,'value':value,'order_by':order_by})

    
    # paginate students
    #paginator = Paginator(students, 3)
    #page = request.GET.get('page')
    #try:
            #students = paginator.page(page)
    #except PageNotAnInteger:
               # If page is not an integer, deliver first page.
            #students = paginator.page(1)
    #except EmptyPage:
                # If page is out of range (e.g. 9999), deliver
                # last page of results.
            #students = paginator.page(paginator.num_pages)

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s </h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)