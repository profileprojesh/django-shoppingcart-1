from django import template
from item.models import Order

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        order = Order.objects.filter(receiver=user, ordered=False)
        if order.exists():
            order = order[0]
            return order.items.count()
        else:
            return 0
    else:
        return 0            


