from tools.models import Access
from datetime import datetime, timedelta
import time
from django.http import JsonResponse, HttpResponse

# Create your views here.


def Timestamp(date, num=1):
    timeInt = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
    return int(round(timeInt * num))


def Visitor(request):
    data = []
    day = request.GET.get('days', None)
    access_list = Access.objects.all()
    if day:
        num = len(access_list) - int(day)
        access_list = access_list[0 if num < 0 else num:]
    for access in access_list:
        data.append([Timestamp(access.date.strftime(
            '%Y-%m-%d %H:%M:%S'), 1000), access.num])
    return JsonResponse(data, safe=False)


def accessViews(request):
    today = datetime.strptime(
        datetime.now().strftime('%Y-%m-%d 08:00:00'),
        "%Y-%m-%d %H:%M:%S")
    if today.hour < 8:
        today = today + timedelta(hours=8 - today.hour)
    if today.hour > 8:
        today = today - timedelta(hours=today.hour - (today.hour - 8))
    try:
        access = Access.objects.get(date=today)
        access.num = int(access.num) + 1
    except BaseException:
        access = Access(date=today, num=1)
    access.save()
    return HttpResponse(bytes('{}'.format(datetime.now()), 'utf-8'))
