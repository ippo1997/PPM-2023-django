from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('item.Item')
    status = models.CharField(max_length=255, choices=(
        ('processing', 'In elaborazione'),
    ))
    shipping_status = models.CharField(max_length=255, choices=(
        ('not_shipped', 'Non spedito'),
        ('shipped', 'Spedito'),
    ), default='not_shipped')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ordine #{self.pk}"