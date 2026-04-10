from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment

@login_required
def payment_view(request, pk):
    payment = get_object_or_404(Payment, pk=pk, registration__user=request.user)
    if payment.payment_status == 'paid':
        messages.info(request, 'Payment already completed.')
        return redirect('registrations:my_registrations')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pay':
            payment.payment_status = 'paid'
            payment.save()
            messages.success(request, f'Payment of \u20b9{payment.amount} completed! Transaction ID: {payment.transaction_id}')
            return redirect('registrations:my_registrations')
        elif action == 'fail':
            payment.payment_status = 'failed'
            payment.save()
            messages.error(request, 'Payment failed. You can retry later.')
            return redirect('registrations:my_registrations')
    return render(request, 'payments/payment.html', {'payment': payment})

@login_required
def payment_history(request):
    payments = Payment.objects.filter(
        registration__user=request.user
    ).select_related('registration__event')
    return render(request, 'payments/payment_history.html', {'payments': payments})
