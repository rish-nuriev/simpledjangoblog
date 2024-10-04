from django.shortcuts import render
from django.http import JsonResponse
from services import email_sender

from .forms import SubscriptionForm


def subscribe(request):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email_sender.send(form.instance.email, 'Спасибо за подписку!')
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors})
    else:
        form = SubscriptionForm()
        return render(request, 'subscription/form.html',
                      context={'subscription_form': form})
