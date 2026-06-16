from django.db import models

KATEGORIE = [
    ('jedzenie', 'Jedzenie'),
    ('transport', 'Transport'),
    ('rozrywka', 'Rozrywka'),
    ('zdrowie', 'Zdrowie'),
    ('inne', 'Inne'),
]

class Wydatek(models.Model):
    nazwa = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.CharField(max_length=50, choices=KATEGORIE)
    data = models.DateField()

    def __str__(self):
        return f"{self.nazwa} - {self.kwota} zł"