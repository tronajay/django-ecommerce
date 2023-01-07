from django.db import models
from base.models import BaseModel
from product.models import Product
from accounts.models import User

# Create your models here.
class Order(BaseModel):
    order_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LineItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
