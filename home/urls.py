from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('cus/', views.cus),
    path('cons/', views.cons),
    path('crm/', views.crm),
    path('ma/', views.ma),
    path('emp/', views.emp),
    path('sch/', views.sch),
]