from ..models import Order,Orderdetails
from django import template

register = template.Library()

@register.filter
def count_product(user):
    if user.is_authenticated:
      order=Order.objects.filter(user=user,is_finshied=False)
      if order.exists():
         return order[0].orderdetails_order.count()
    return 0


