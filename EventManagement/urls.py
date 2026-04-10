from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('events/', include('events.urls', namespace='events')),
    path('registrations/', include('registrations.urls', namespace='registrations')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
