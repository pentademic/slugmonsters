from django.urls import path
from . import views

urlpatterns = [
    path('', views.slug_list, name='slug_list'),
    path('slug/<str:id_slug>/', views.slug_detail, name='slug_detail'),
    path('equipement/<str:id_equip>/', views.equipement_detail, name='equipement_detail'),
    path('slug/<str:id_slug>/?<str:message>', views.slug_detail, name='slug_detail_mes'),
    path('update_audio_state/', views.update_audio_state, name='update_audio_state'),
]