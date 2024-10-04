from django import template
from subscription.forms import SubscriptionForm

register = template.Library()


@register.inclusion_tag('subscription/form.html')
def subscription_form():
    subscription_form = SubscriptionForm()
    return {'subscription_form': subscription_form}
