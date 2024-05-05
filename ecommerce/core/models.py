from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User, AbstractUser


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


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Address"


class Evento(models.Model):
    nome = models.CharField(max_length=200)
    punteggio = models.IntegerField()

    def __str__(self):
        return self.nome

class CustomUser(AbstractUser):
    eventi_partecipati = models.ManyToManyField(Evento, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',  # Modifica l'argomento related_name
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # Modifica l'argomento related_name
        related_query_name='user'
    )

    def __str__(self):
        return self.username
