# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from ..models.groups import  Group
from django.template import Context, Template 
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib import messages
#from django.contrib.messages import constants as messages
from django.views.generic.edit import UpdateView, CreateView
from django.forms import ModelForm 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.contrib.messages.views import SuccessMessageMixin

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        
        fields = ['id','first_name', 'last_name', 'middle_name','birthday','photo','ticket','notes','student_group']
    def __init__(self, *args, **kwargs):
            super(StudentUpdateForm, self).__init__(*args, **kwargs)
            
            self.helper = FormHelper(self)
            try:
                # set form tag attributes
                self.helper.form_action = reverse('students_edit',
                kwargs={'pk': kwargs['instance'].id})
            except:
                self.helper.form_action = reverse('students_add') #add_Student
            self.helper.form_method = 'POST'
            self.helper.form_class = 'form-horizontal'
            # set form field properties
            self.helper.help_text_inline = True
            self.helper.html5_required = True
            self.helper.label_class = 'col-sm-2 control-label'
            self.helper.field_class = 'col-sm-10'
            # add buttons
            self.helper.layout = FormActions('first_name', 'last_name', 'middle_name','birthday','photo','ticket','notes','student_group',
                                    Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                                    Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),)
    
    # Create your views here.
'''
class StudentUpdateView(SuccessMessageMixin, UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    def get_success_url(self):
        return (reverse('home'))
    
    def post(self, request, *args, **kwargs):
        
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.INFO, u'Редагування відмінено!')
            #return HttpResponseRedirect(reverse('home'))
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!'% reverse('home'))
        else:
            messages.add_message(request, messages.SUCCESS, u'Зміни збережено!')
            return super(StudentUpdateView, self).post(request, *args, **kwargs)
'''
class StudentAddView(SuccessMessageMixin,CreateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    def get_success_url(self):
        return (reverse('home'))
    
    
    def post(self, request, *args, **kwargs):
        
        if request.POST.get('cancel_button'):
            messages.add_message(request, messages.INFO, u'Зміни скасовано! ')
            
            return HttpResponseRedirect(reverse('home'))
        else:
            last_name = request.POST.get('last_name', '').strip()
            messages.add_message(request, messages.SUCCESS, u'Студента %s додано!' % last_name)
            return super(StudentAddView, self).post(request, *args, **kwargs)
    
    
# Views for Students
def students_list(request):
    
    students = Student.objects.all()          
    
    
    order_by = request.GET.get('order_by', '')
    if order_by=='':
        students=students.order_by('last_name')
        all_range_students=Student.objects.values_list('id', flat=True).order_by('last_name')
        
    if order_by in ('last_name', 'first_name', 'ticket','id'):
        students = students.order_by(order_by)
        all_range_students=Student.objects.values_list('id', flat=True).order_by(order_by)
        
        
    if request.GET.get('reverse', '') == '1':
        students = students.reverse
        p=Student.objects.values_list('id', flat=True).order_by(order_by)
        all_range_students=p.reverse()
            
    
    try:
        page = int(request.GET.get('page'))
    except: 
        page = 1
    
    # потрібно обчислити змінну all_range_students відповідно до сортування. Передати список id у відсортованому списку
    
    def group(all_range_students, count):
          # """ Группировка элементов последовательности по count элементов """
        return [all_range_students[i:i + count] for i in range(0, len(all_range_students), count)]
    page_all=group(all_range_students,3*page)
    current_page=page + 1 
    
    
    #Список сторінок по їх номерах
    storinka=range(1,len(page_all) +1)
    start_page=page_all.index(page_all[0])+1
    end_page=len(page_all)
    display = 'display:visible'
    if page > end_page:
        display = "display:none";
        
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
           'end_page':end_page,'storinka':storinka,'page':page,'value':value,'order_by':order_by,
           'current_page':current_page,'display':display})

    
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
'''
def students_add(request):
        # Якщо форма була запощена:
        # Якщо кнопка Скасувати була натиснута:
        # Повертаємо користувача до списку студентів
        # Якщо кнопка Додати була натиснута:
        # Перевіряємо дані на коректність та збираємо помилки
        # Якщо дані були введені некоректно:
        # Віддаємо шаблон форми разом із знайденими помилками
        # Якщо дані були введені коректно:
        # Створюємо та зберігаємо студента в базу
        # Повертаємо користувача до списку студентів
        # Якщо форма не була запощена:
        # повертаємо код початкового стану форми
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # TODO: validate input from user
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
            
                else:
                    data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            student_group = request.POST.get('student_group', '').strip() 
            
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            
            
            else:
                groups = Group.objects.filter(pk=student_group)            
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]
            
            photo = request.FILES.get('photo')
            try:
                f_ad_name = (request.FILES.get('photo').content_type).split('/')[0]
            
                
                if photo.size > (2097152):   
                    errors['photo'] = u"Максимальний розмір зображення має бути< 2Mb"
                        #f_ad_name = (photo.name).split('.')[1];
            #if not  (f_ad_name == 'bmp' or f_ad_name =='jpg'
                     #or f_ad_name =='png' or f_ad_name =='gif' or f_ad_name =='jpeg'):
                #errors['photo'] = u"Допустимий формат bmp,jpg,png,gif"
                if  f_ad_name != 'image' :
                    errors['photo'] = u"Допустимий формат bmp,jpg,png,gif,jpeg"
                else:
                    data['photo'] = photo
            except:
                    pass
            
          
            # save student
            if not errors:
                student = Student(**data)
                student.save()
                # redirect to students list
                #return HttpResponseRedirect(u'%s?status_message=Студента  %s %s  успішно додано!'% (reverse('home'),first_name,last_name))
                messages.success(request, u'Студента %s %s успішно додано!'%(first_name,last_name))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),'errors': errors})
            
            
            
            
            
            if not errors:
                # create student object
                student = Student(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                middle_name=request.POST['middle_name'],
                birthday=request.POST['birthday'],
                ticket=request.POST['ticket'],
                student_group=Group.objects.get(pk=request.POST['student_group']),
                photo=request.FILES['photo'],)
                # save it to database
                student.save()
                # redirect user to students list
                return HttpResponseRedirect(u'%s?status_message=Студента  успішно додано!'% reverse('home'))
                
                
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',{'groups': Group.objects.all().order_by('title'),
                'errors': errors})
        elif request.POST.get('cancel_button') is not None:
                # redirect to home page on cancel button
                #return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
                #MESSAGE_TAGS = {messages.INFO: u'Додавання студента скасовано!',}
                messages.info(request, u'Додавання студента скасовано!')
                #messages.add_message(request, messages.INFO, 'Додавання студента скасовано!')
                #return render(request, 'students/students_list.html', MESSAGE_TAGS)
                #return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home'),MESSAGE_TAGS ) )
                return HttpResponseRedirect(reverse('home'))
    else:
                # initial form render
                return render(request, 'students/students_add.html',{'groups': Group.objects.all().order_by('title')})
            
'''
    
    

def students_edit(request,pk):
    if request.method == "GET":
        student = Student.objects.filter(id=pk)
        data =  {   'first_name': student.values_list('first_name')[0][0],
                    'last_name': student.values_list('last_name')[0][0],
                    'middle_name': student.values_list('middle_name')[0][0],
                    'birthday': (student.values_list('birthday')[0][0]).isoformat(),
                    'photo':student.values_list('photo')[0][0],
                    'ticket': student.values_list('ticket')[0][0],
                    'groups':Group.objects.filter(pk=(student.values_list('group')[0][0])),
                    'group_ident':student.values_list('student_group')[0][0],
                    'group_all': Group.objects.all(),
                    'notes': student.values_list('ticket')[0][0],
                    
            }
        return render(request, 'students/students_edit1.html', data)
    if request.method == "POST":
        # was form add button clicked?
        
        
        if request.POST.get('add_button') is not None:
            # TODO: validate input from user
            
            errors = {}
            # validate student data will go here
            data_new = {'middle_name': request.POST.get('middle_name'),'notes': request.POST.get('notes')}
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data_new['first_name'] = first_name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data_new['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
            
                else:
                    data_new['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data_new['ticket'] = ticket
            
            student_group = request.POST.get('student_group', '') 
            #student_group = request.POST.get('student_group')
            #g=Group.objects.values('id','title')
            #val_gr = {}
            #for i in g:
                #value.update({i['title']:i['id']})
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            
            
            else:
                groups = Group.objects.filter(pk=student_group)            
                if student_group == 0:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data_new['student_group'] = groups[0]
            
            photo = request.FILES.get('photo')
            try:
                f_ad_name = (request.FILES.get('photo').content_type).split('/')[0]
            
                
                if photo.size > (2097152):   
                    errors['photo'] = u"Максимальний розмір зображення має бути< 2Mb"
                        #f_ad_name = (photo.name).split('.')[1];
            #if not  (f_ad_name == 'bmp' or f_ad_name =='jpg'
                     #or f_ad_name =='png' or f_ad_name =='gif' or f_ad_name =='jpeg'):
                #errors['photo'] = u"Допустимий формат bmp,jpg,png,gif"
                if  f_ad_name != 'image' :
                    errors['photo'] = u"Допустимий формат bmp,jpg,png,gif,jpeg"
                else:
                    data_new['photo'] = photo
            except:
                    pass
            
          
            # save student
            if not errors:
                
                data_new['id'] = pk
                student = Student(**data_new)
                student.save(force_update=True)
                # redirect to students list
                #return HttpResponseRedirect(u'%s?status_message=Студента  %s %s  успішно додано!'% (reverse('home'),first_name,last_name))
                messages.success(request, u'Студента %s %s успішно збережено!'%(first_name,last_name))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_edit1.html',
                    {'groups': Group.objects.all().order_by('title'),'errors': errors})
            
            
            
            
            
            if not errors:
                # create student object
                student = Student(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                middle_name=request.POST['middle_name'],
                birthday=request.POST['birthday'],
                ticket=request.POST['ticket'],
                student_group=Group.objects.get(pk=request.POST['student_group']),
                photo=request.FILES['photo'],)
                # save it to database
                
                # redirect user to students list
                return HttpResponseRedirect(u'%s?status_message=Студента  успішно додано!'% reverse('home'))
                
                
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_edit1.html',{'groups': Group.objects.all().order_by('title'),
                'errors': errors})
        elif request.POST.get('cancel_button') is not None:
                # redirect to home page on cancel button
                #return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
                #MESSAGE_TAGS = {messages.INFO: u'Додавання студента скасовано!',}
                messages.info(request, u'Редагування студента скасовано!')
                #messages.add_message(request, messages.INFO, 'Додавання студента скасовано!')
                #return render(request, 'students/students_list.html', MESSAGE_TAGS)
                #return HttpResponseRedirect(u'%s?status_message=%s' % (reverse('home'),MESSAGE_TAGS ) )
                return HttpResponseRedirect(reverse('home'))
    else:
                # initial form render
                return render(request, 'students/students_edit1.html',{'groups': Group.objects.all().order_by('title')})

    #return render(request, 'students/students_edit1.html', data)
    

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s </h1>' % sid)
