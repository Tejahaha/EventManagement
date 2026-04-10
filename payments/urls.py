from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:pk>/pay/', views.payment_view, name='pay'),
    path('history/', views.payment_history, name='history'),
]
