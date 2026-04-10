from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Registration
from events.models import Event
from payments.models import Payment

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.status in ['completed', 'cancelled']:
        messages.error(request, 'Registration is not available for this event.')
        return redirect('events:detail', pk=pk)

    if event.is_full():
        messages.error(request, 'Sorry, this event is fully booked.')
        return redirect('events:detail', pk=pk)

    existing = Registration.objects.filter(user=request.user, event=event).first()
    if existing:
        if existing.status == 'active':
            messages.warning(request, 'You are already registered for this event.')
            return redirect('events:detail', pk=pk)
        elif existing.status == 'cancelled':
            existing.status = 'active'
            existing.save()
            event.available_seats -= 1
            event.save()
            _create_payment(existing, event)
            messages.success(request, 'Re-registration successful!')
            return redirect('registrations:my_registrations')

    registration = Registration.objects.create(user=request.user, event=event)
    event.available_seats -= 1
    event.save()

    payment = _create_payment(registration, event)

    # Send confirmation email (will work after email placeholders are filled)
    try:
        send_mail(
            subject=f'Registration Confirmed: {event.title}',
            message=f'Hi {request.user.username},\n\nYour registration for "{event.title}" is confirmed.\nRegistration ID: {registration.registration_id}\nDate: {event.date} at {event.time}\nVenue: {event.venue}\n\nThank you!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=True,
        )
    except Exception:
        pass

    if event.is_free():
        messages.success(request, f'Successfully registered for {event.title}! (Free event)')
        return redirect('registrations:my_registrations')
    else:
        messages.success(request, f'Registered! Please complete your payment.')
        return redirect('payments:pay', pk=payment.pk)

def _create_payment(registration, event):
    payment, created = Payment.objects.get_or_create(
        registration=registration,
        defaults={
            'amount': event.ticket_price,
            'payment_status': 'paid' if event.is_free() else 'pending',
        }
    )
    return payment

@login_required
def cancel_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    if registration.status == 'cancelled':
        messages.warning(request, 'Registration is already cancelled.')
        return redirect('registrations:my_registrations')
    registration.status = 'cancelled'
    registration.save()
    event = registration.event
    event.available_seats += 1
    event.save()
    messages.success(request, f'Registration for {event.title} cancelled.')
    return redirect('registrations:my_registrations')

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event', 'event__category')
    return render(request, 'registrations/my_registrations.html', {'registrations': registrations})
