from django import template

from ..models import Payment

register = template.Library()

@register.inclusion_tag("app/payment_tags.html", takes_context=True)
def get_amount(context):
    payment = Payment.objects.all().last()
    context['payment'] = payment
    return context


@register.simple_tag
def current_title():
    return 'KindleCoverFactory'
