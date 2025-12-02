from django.db import models
from django.contrib.auth.models import User


class Atelier(models.Model):
    TITRE_CHOICES = [
        ('3D', 'Impression 3D'),
        ('LASER', 'Découpe Laser'),
        ('ELEC', 'Électronique & Arduino'),
        ('REPAR', 'Réparation & Upcycling'),
    ]
    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=5, choices=TITRE_CHOICES, default='3D')
    description = models.TextField()
    date_debut = models.DateTimeField()
    lieu = models.CharField(max_length=200, default="Fablab Handimaker - St Denis")
    image = models.ImageField(upload_to='ateliers/', blank=True, null=True)
    capacite_max = models.PositiveIntegerField(default=8)
    participants = models.ManyToManyField(User, related_name='ateliers_inscrits', blank=True)
    createur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['date_debut']

    def places_restantes(self):
        return self.capacite_max - self.participants.count()

    def __str__(self):
        return self.titre


class Realisation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    maker = models.ForeignKey(User, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='realisations/')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titre} - {self.maker.username}"
