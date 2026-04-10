import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from accounts.models import CustomUser
from events.models import Event
from registrations.models import Registration
from payments.models import Payment
from attendance.models import Attendance

def generate_chart(labels, values, title, color='steelblue', chart_type='bar'):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    if chart_type == 'bar':
        ax.bar(labels, values, color=color)
    elif chart_type == 'pie' and sum(values) > 0:
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
    ax.set_title(title, fontsize=11)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=80)
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return chart

@login_required
def dashboard_index(request):
    user = request.user
    if user.is_admin():
        return admin_dashboard(request)
    elif user.is_organizer():
        return organizer_dashboard(request)
    else:
        return participant_dashboard(request)

def admin_dashboard(request):
    total_users = CustomUser.objects.filter(role='participant').count()
    total_organizers = CustomUser.objects.filter(role='organizer').count()
    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    total_payments = Payment.objects.filter(payment_status='paid').aggregate(total=Sum('amount'))['total'] or 0

    events = Event.objects.annotate(reg_count=Count('registrations'))[:8]
    labels = [e.title[:15] for e in events]
    values = [e.reg_count for e in events]
    reg_chart = generate_chart(labels, values, 'Registrations per Event') if labels else None

    context = {
        'role': 'admin',
        'total_users': total_users,
        'total_organizers': total_organizers,
        'total_events': total_events,
        'total_registrations': total_registrations,
        'total_payments': total_payments,
        'reg_chart': reg_chart,
        'recent_registrations': Registration.objects.select_related('user', 'event').order_by('-registered_at')[:10],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

def organizer_dashboard(request):
    my_events = Event.objects.filter(organizer=request.user).annotate(reg_count=Count('registrations'))
    total_revenue = Payment.objects.filter(
        registration__event__organizer=request.user, payment_status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_attendance = Attendance.objects.filter(
        registration__event__organizer=request.user, attendance_status='present'
    ).count()

    labels = [e.title[:15] for e in my_events[:8]]
    reg_values = [e.reg_count for e in my_events[:8]]
    reg_chart = generate_chart(labels, reg_values, 'Registrations per Event', '#28a745') if labels else None

    rev_values = []
    for e in my_events[:8]:
        rev = Payment.objects.filter(
            registration__event=e, payment_status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0
        rev_values.append(float(rev))
    rev_chart = generate_chart(labels, rev_values, 'Revenue per Event (\u20b9)', '#fd7e14') if labels else None

    context = {
        'role': 'organizer',
        'my_events': my_events,
        'total_revenue': total_revenue,
        'total_attendance': total_attendance,
        'reg_chart': reg_chart,
        'rev_chart': rev_chart,
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)

def participant_dashboard(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    payments = Payment.objects.filter(registration__user=request.user).select_related('registration__event')
    attendance_records = Attendance.objects.filter(registration__user=request.user).select_related('registration__event')

    att_labels = ['Present', 'Absent']
    present_count = attendance_records.filter(attendance_status='present').count()
    absent_count = attendance_records.filter(attendance_status='absent').count()
    att_chart = generate_chart(att_labels, [present_count, absent_count], 'Attendance Summary', chart_type='pie') if (present_count + absent_count) > 0 else None

    context = {
        'role': 'participant',
        'registrations': registrations,
        'payments': payments,
        'attendance_records': attendance_records,
        'att_chart': att_chart,
        'present_count': present_count,
        'absent_count': absent_count,
    }
    return render(request, 'dashboard/participant_dashboard.html', context)
