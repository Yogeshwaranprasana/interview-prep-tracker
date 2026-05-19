from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('add/', views.add_skill, name='add_skill'),
    path('edit/<int:id>/', views.edit_skill, name='edit_skill'),
    path('delete/<int:id>/', views.delete_skill, name='delete_skill'),
]
