#! /usr/bin/python3
# -*- coding:UTF-8 -*-
# time : 2019/4/15  14:03
# file : views.py
# By 卤蛋
from django.template import loader
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,
)
template_name = "error.html"
template = loader.get_template(template_name)


def server_error(request):
    info = '500服务器错误'
    return HttpResponseServerError(template.render(locals()), content_type='text/html')


def page_not_found(request, exception):
    info = '404页面没有找到'
    return HttpResponseNotFound(template.render(locals()), content_type='text/html')


def permission_denied(request, exception):
    info = '403没有权限'
    return HttpResponseForbidden(template.render(locals()), content_type='text/html')


def bad_request(request, exception):
    info = '400错误的请求'
    return HttpResponseBadRequest(template.render(locals()), content_type='text/html')
