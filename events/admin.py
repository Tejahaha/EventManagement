from django.contrib import admin
from .models import Event, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'category', 'date', 'status', 'available_seats', 'ticket_price']
    list_filter = ['status', 'category']
    search_fields = ['title', 'venue']
