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
    punteggio_squadra = models.IntegerField()  # Assicurati che questo attributo sia definito correttamente

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


from django.db import models

class Squadra(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Azione(models.Model):
    descrizione = models.CharField(max_length=255)
    punti = models.IntegerField()
    azione_esclusiva = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descrizione} [{self.punti} punti]"


class SquadraAzione(models.Model):
    squadra = models.ForeignKey(Squadra, on_delete=models.CASCADE)
    azione = models.ForeignKey(Azione, on_delete=models.CASCADE)
    completata = models.BooleanField(default=False)
