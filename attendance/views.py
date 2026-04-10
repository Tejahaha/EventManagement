from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from registrations.models import Registration
from events.models import Event

@login_required
def mark_attendance(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if event.organizer != request.user and not request.user.is_admin():
        messages.error(request, 'Only the organizer can mark attendance.')
        return redirect('events:detail', pk=event_pk)

    registrations = Registration.objects.filter(event=event, status='active').select_related('user')

    if request.method == 'POST':
        for reg in registrations:
            status = request.POST.get(f'attendance_{reg.pk}', 'absent')
            Attendance.objects.update_or_create(
                registration=reg,
                defaults={'attendance_status': status}
            )
        messages.success(request, 'Attendance marked successfully!')
        return redirect('events:detail', pk=event_pk)

    attendance_data = []
    for reg in registrations:
        att = Attendance.objects.filter(registration=reg).first()
        attendance_data.append({'registration': reg, 'attendance': att})

    return render(request, 'attendance/mark_attendance.html', {
        'event': event,
        'attendance_data': attendance_data,
    })

@login_required
def attendance_history(request):
    from registrations.models import Registration
    registrations = Registration.objects.filter(user=request.user, status='active')
    history = []
    for reg in registrations:
        att = Attendance.objects.filter(registration=reg).first()
        history.append({'registration': reg, 'attendance': att})
    return render(request, 'attendance/attendance_history.html', {'history': history})
