from . import views
from django.urls import path

urlpatterns = [
    path('Visitor', views.Visitor, name='Visitorjson'),
    path('access', views.accessViews, name='access')
]
