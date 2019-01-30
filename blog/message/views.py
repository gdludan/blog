from django.shortcuts import render,redirect
from django.template import RequestContext
from .models import Message
from blog import paginatorPage,timeago_or_time
from django.conf import settings
from django.http import JsonResponse
from user.models import MyUser as User
from .models import Type
from django.contrib.auth.decorators import login_required

# Create your views here.
def messageIndexVisw(request):
    if not request.user.id:
        info='你还没有登录，此页面不能显示内容'
    else:
        user = User.objects.get(id = request.user.id)
        message_list = Message.objects.order_by('-time').filter(user=user).all()
        for message in message_list:
            message.time=timeago_or_time(message.time,True)
        paginator,pageInfo= paginatorPage(message_list,settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)#文章分页
    return render(request,'message.html',locals(),RequestContext(request))

@login_required
def set(request,user):
    user = User.objects.get(id = user)
    if user.id != request.user.id :return JsonResponse({'status': 401, 'message': '权限错误'})
    content = request.GET.get('content','')
    type = Type.objects.get(id = int(request.GET.get('type','')))
    message = Message(content=content,view=0,type=type,user=user,ip=request.META['REMOTE_ADDR'])
    if message.save():
        res = {'status': 0, 'message': '保存失败'}
    else:
        res = {'status': 1, 'message': '保存成功'}
        res['data']={"content":content,"view":0,'ip':request.META['REMOTE_ADDR']}
    return JsonResponse(res)

# @login_required
# def unread(request,user):
#     user = User.objects.get(id=user)
#     if user.id != request.user.id : return JsonResponse({'status': 401, 'message': '权限错误'})
#     res = {'status': 0, 'message': '未知错误','data':[]}
#     for i in Message.objects.order_by('-time').filter(user=user, view=0):
#          res['data'].append({"id":i.id,"content":i.content,'time':i.time,'view':i.view,'type':i.type.type_name})
#     return JsonResponse(res)

@login_required
def setread(request,user):
    user = User.objects.get(id=user)
    res = {'status': 1, 'message': '成功'}
    if user.id != request.user.id : return JsonResponse({'status': 401, 'message': '权限错误'})
    for mess in Message.objects.order_by('-time').filter(user=user, view=0):
        if mess.user.id != request.user.id: return JsonResponse({'status': 401, 'message': '权限错误'})
        mess.view=1
        mess.save()
    return JsonResponse(res)

@login_required
def setmess(request):
    res = {'status': 1, 'message': '成功'}
    mess = Message.objects.filter(id=int(request.GET.get('id',''))).first()
    if not mess :return JsonResponse({'status': 0, 'message': '没有找到数据'})
    if mess.user.id != request.user.id : return JsonResponse({'status': 401, 'message': '权限错误'})
    else:
        mess.view=1
        if not mess.save():res = {'status': 0, 'message': '设置成功','content':mess.content}
    return JsonResponse(res)

@login_required
def delread(request,user):
    res = {'status': 1, 'message': '成功','set':True}
    if not request.user.id : return JsonResponse({'status': 0, 'message': '失败','set':False})
    user = User.objects.get(id=user)
    for mess in Message.objects.filter(user=user, view=1):
        if mess.user.id != request.user.id : return JsonResponse({'status': 401, 'message': '权限错误'})
        mess.delete()
    return JsonResponse(res)

def num(request):
    res = {'status': 1, 'message': '成功','num':0,'set':True}
    if not request.user.id : return JsonResponse({'status': 0, 'message': '失败','num':0,'set':False})
    user = User.objects.get(id=request.user.id)
    i,len_num = 0,0
    for mess in Message.objects.order_by('-time').filter(user=user):
        if mess.view == 0 :i=i+1
        len_num=len_num+1
    res['num'],res['len']=i,len_num
    return JsonResponse(res)