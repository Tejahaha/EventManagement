from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from events.models import Event
from registrations.models import Registration
from attendance.models import Attendance

@login_required
def submit_feedback(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    if event.status != 'completed':
        messages.error(request, 'Feedback can only be submitted for completed events.')
        return redirect('events:detail', pk=event_pk)

    registration = Registration.objects.filter(user=request.user, event=event, status='active').first()
    if not registration:
        messages.error(request, 'You must be registered to leave feedback.')
        return redirect('events:detail', pk=event_pk)

    attendance = Attendance.objects.filter(registration=registration, attendance_status='present').first()
    if not attendance:
        messages.error(request, 'Only attendees who were marked present can leave feedback.')
        return redirect('events:detail', pk=event_pk)

    existing = Feedback.objects.filter(user=request.user, event=event).first()
    if existing:
        messages.warning(request, 'You have already submitted feedback for this event.')
        return redirect('events:detail', pk=event_pk)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.event = event
            feedback.save()
            messages.success(request, 'Feedback submitted. Thank you!')
            return redirect('events:detail', pk=event_pk)
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback_form.html', {'form': form, 'event': event})
