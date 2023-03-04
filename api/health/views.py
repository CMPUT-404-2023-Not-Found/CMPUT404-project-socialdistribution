# health/views
# 2023-02-08

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.http import FileResponse

# Create your views here.
def now(request):
    # ver = staticfiles_storage.url('ver.txt')
    return FileResponse(open('health/ver.txt', 'rb'))
