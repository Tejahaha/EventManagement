from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('event/<int:pk>/register/', views.register_for_event, name='register'),
    path('<int:pk>/cancel/', views.cancel_registration, name='cancel'),
    path('my/', views.my_registrations, name='my_registrations'),
]
