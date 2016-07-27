from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from .models.students import Student
from .models.groups import Group
from .models.journal import Journal
from .models.exam import Examen
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Journal)
admin.site.register(Examen)