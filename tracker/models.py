from django.db import models
from django.contrib.auth.models import User

KATEGORIE = [
    ('jedzenie', 'Jedzenie'),
    ('transport', 'Transport'),
    ('rozrywka', 'Rozrywka'),
    ('zdrowie', 'Zdrowie'),
    ('inne', 'Inne'),
]

class Wydatek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.CharField(max_length=50, choices=KATEGORIE)
    data = models.DateField()
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nazwa} - {self.kwota} zł"

class Przychod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opis = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.opis} - {self.kwota} zł"

class Cel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=200)
    kwota_docelowa = models.DecimalField(max_digits=10, decimal_places=2)
    kwota_odlozona = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    termin = models.DateField(null=True, blank=True)
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return self.nazwa

    def procent(self):
        if self.kwota_docelowa > 0:
            return min(int((self.kwota_odlozona / self.kwota_docelowa) * 100), 100)
        return 0