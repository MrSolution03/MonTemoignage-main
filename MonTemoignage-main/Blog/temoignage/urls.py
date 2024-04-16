from django.urls import path
from . import views

urlpatterns = [
    path('',views.acceuil,name='acceuil'),
    path('recevoirJesus/',views.recevoirJesus,name='recevoirJesus'),
    path('notreEquipe/',views.notreEquipe,name='notreEquipe'),
    path('contact/',views.contact,name='contact'),
    path('video/',views.video,name='video'),
    path('text/',views.text,name='text'),
    path('player_video/<slug:slug>/',views.player_video,name='player_video'),
    path('player_text/<slug:slug>/',views.player_text,name='player_text'),
]
