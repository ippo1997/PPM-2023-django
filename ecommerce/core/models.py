from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('item.Item')
    status = models.CharField(max_length=255, choices=(
        ('pending_payment', 'In attesa di pagamento'),
        ('processing', 'In elaborazione'),
        ('shipped', 'Spedito'),
    ))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ordine #{self.pk}"
