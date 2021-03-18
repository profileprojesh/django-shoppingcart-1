from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

PRODUCT_CATEGORY=(
    ('E', 'ELECTRONIC'),
    ('FW', 'FOOT-WEAR'),
    ('MF', 'MENS FASHION'),
    ('WF', 'WOMENS FASHION'),
    ('MP', 'MOBILE PHONE'),
    ('OT', 'OTHERS'),
)

class Product(models.Model):
    title = models.CharField(max_length=30)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=PRODUCT_CATEGORY, max_length=3, default='OT')
    image = models.ImageField(upload_to='cart_images')

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        output = (300, 300)
        if img.width >300 or img.height >300:
            img.thumbnail(output)
        img.save(self.image.path)

    def __str__(self):
        return  self.title  



class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item.title)

    @property
    def get_total_item(self):
        return self.quantity*self.item.price    

class Order(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    order_created = models.DateField(auto_now_add=True)

    def get_grand_order_total(self):
        orderitems = self.items.all()
        total= sum([item.get_total_item for item in orderitems])
        return total

    @property
    def get_cart_size(self):
        return self.items.all().count()    


    def __str__(self):
        return str(self.order_created)

class OrderInfo(models.Model):
    orderid = models.CharField(max_length=12, null=True, blank=True)
    orderlist = models.ForeignKey(Order, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete =models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=12)
    ordered_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20)


    def __str__(self):
        return f'{self.name} with address of {self.orderid}'


class Updates(models.Model):
    message = models.TextField()

    def __str__(self):
        return str(self.id)

class Status(models.Model):
    orderinfo = models.OneToOneField(OrderInfo, on_delete = models.CASCADE)
    delivered = models.BooleanField(default=False)
    messages = models.ManyToManyField(Updates)

    def __str__(self):
        return self.delivered














