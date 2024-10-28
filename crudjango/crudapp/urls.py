from django.urls import path
from . import views

urlpatterns = [
    path('', views.person_list, name='person_list'),
    path('create/', views.create_person, name='create_person'),
    path('update/<int:pk>/', views.update_person, name='update_person'),
    path('delete/<int:pk>/', views.delete_person, name='delete_person'),
]
