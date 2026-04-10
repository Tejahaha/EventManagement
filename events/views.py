import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Event, Category
from .forms import EventForm, CategoryForm
from registrations.models import Registration

def home_view(request):
    events = Event.objects.filter(status__in=['upcoming', 'ongoing']).order_by('date')[:6]
    categories = Category.objects.all()
    return render(request, 'events/home.html', {'events': events, 'categories': categories})

def event_list_view(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price_filter = request.GET.get('price', '')
    status_filter = request.GET.get('status', '')

    if query:
        events = events.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        events = events.filter(category__id=category_id)
    if price_filter == 'free':
        events = events.filter(ticket_price=0)
    elif price_filter == 'paid':
        events = events.filter(ticket_price__gt=0)
    if status_filter:
        events = events.filter(status=status_filter)

    context = {
        'events': events,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'price_filter': price_filter,
        'status_filter': status_filter,
    }
    return render(request, 'events/event_list.html', context)

def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    user_registration = None
    feedbacks = event.feedbacks.all()
    avg_rating = None
    if feedbacks.exists():
        avg_rating = round(sum(f.rating for f in feedbacks) / feedbacks.count(), 1)
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(user=request.user, event=event).first()
        is_registered = user_registration is not None and user_registration.status == 'active'
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'user_registration': user_registration,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
    })

@login_required
def create_event_view(request):
    if not request.user.is_organizer() and not request.user.is_admin():
        messages.error(request, 'Only organizers can create events.')
        return redirect('events:list')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.available_seats = event.total_seats
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})

@login_required
def edit_event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user and not request.user.is_admin():
        messages.error(request, 'You are not authorized to edit this event.')
        return redirect('events:detail', pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated = form.save(commit=False)
            seats_diff = updated.total_seats - event.total_seats
            updated.available_seats = max(0, event.available_seats + seats_diff)
            updated.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('events:detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Edit Event', 'event': event})

@login_required
def delete_event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user and not request.user.is_admin():
        messages.error(request, 'You are not authorized to delete this event.')
        return redirect('events:detail', pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('events:list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def export_registrations_csv(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user and not request.user.is_admin():
        messages.error(request, 'Not authorized.')
        return redirect('events:detail', pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.title}_registrations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Registration ID', 'User', 'Email', 'Registered At', 'Status', 'Payment Status'])
    for reg in event.registrations.all():
        payment_status = reg.payment.payment_status if hasattr(reg, 'payment') else 'N/A'
        writer.writerow([
            reg.registration_id, reg.user.username, reg.user.email,
            reg.registered_at.strftime('%Y-%m-%d %H:%M'), reg.status, payment_status
        ])
    return response
