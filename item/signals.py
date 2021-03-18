from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import OrderInfo
from .utils import create_order_id

@receiver(pre_save, sender = OrderInfo)
def create_orderid(sender, instance, **kwargs):
    print(f' orderid is {create_order_id()}')
    instance.orderid = create_order_id()
    print(f'instance is {instance}')


