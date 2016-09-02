
from .settings import PORTAL_URL


def students_proc(request):
     return {'PORTAL_URL': PORTAL_URL}
'''
# -*- coding: utf-8 -*-

def students_proc(request):
    PORTAL_URL = request.scheme + '://' + request.get_host()
    return {'PORTAL_URL': PORTAL_URL}
'''