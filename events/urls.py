from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list_view, name='list'),
    path('<int:pk>/', views.event_detail_view, name='detail'),
    path('create/', views.create_event_view, name='create'),
    path('<int:pk>/edit/', views.edit_event_view, name='edit'),
    path('<int:pk>/delete/', views.delete_event_view, name='delete'),
    path('<int:pk>/export/', views.export_registrations_csv, name='export_csv'),
]
