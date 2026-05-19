from django.urls import path
from . import views

urlpatterns = [

    path(
        'add-application/',
        views.add_application,
        name='add_application'
    ),
   
    path(
    'delete-application/<int:id>/',
    views.delete_application,
    name='delete_application'
),
    path(
    'edit-application/<int:id>/',
    views.edit_application,
    name='edit_application'
),
]