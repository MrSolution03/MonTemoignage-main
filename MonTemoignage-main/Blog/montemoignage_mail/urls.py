from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_email,name='admin_email'),
]
