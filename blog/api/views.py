from django.shortcuts import render
from tools.models import Access
from datetime import datetime,timedelta
import time
from django.http import JsonResponse,HttpResponse

# Create your views here.

def Timestamp(date,num=1):
    timeInt = time.mktime(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
    return int(round(timeInt*num))


def Visitor(request):
    data = []
    day = request.GET.get('days',None)
    access_list = Access.objects.all()
    if day:
        num = len(access_list) - int(day)
        access_list = access_list[0 if num <0 else num:]
    for access in access_list:
        data.append([Timestamp(access.date.strftime('%Y-%m-%d %H:%M:%S'),1000),access.num])
    return JsonResponse(data,safe=False)

def accessViews(request):
    today = datetime.now().strftime('%Y-%m-%d 16:00:00.000000')
    try:
        access = Access.objects.get(date=today)
        access.num = str(int(access.num)+1)
    except:
        access = Access(date=today, num=1)
    access.save()
    return HttpResponse(bytes('{}'.format(datetime.now()),'utf-8'))
