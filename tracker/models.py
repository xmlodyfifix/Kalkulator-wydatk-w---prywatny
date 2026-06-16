from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

KATEGORIE = [
    ('jedzenie', 'Jedzenie'),
    ('transport', 'Transport'),
    ('rozrywka', 'Rozrywka'),
    ('zdrowie', 'Zdrowie'),
    ('inne', 'Inne'),
]

class Gospodarstwo(models.Model):
    nazwa = models.CharField(max_length=200)
    uzytkownicy = models.ManyToManyField(User, related_name='gospodarstwa')

    def __str__(self):
        return self.nazwa

class Wydatek(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gospodarstwo = models.ForeignKey(Gospodarstwo, on_delete=models.SET_NULL, null=True, blank=True)
    nazwa = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    kategoria = models.CharField(max_length=50, choices=KATEGORIE)
    data = models.DateField()
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nazwa} - {self.kwota} zł"

class Przychod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gospodarstwo = models.ForeignKey(Gospodarstwo, on_delete=models.SET_NULL, null=True, blank=True)
    opis = models.CharField(max_length=200)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.opis} - {self.kwota} zł"

class Cel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gospodarstwo = models.ForeignKey(Gospodarstwo, on_delete=models.SET_NULL, null=True, blank=True)
    nazwa = models.CharField(max_length=200)
    kwota_docelowa = models.DecimalField(max_digits=10, decimal_places=2)
    kwota_odlozona = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    termin = models.DateField(null=True, blank=True)
    wspolne = models.BooleanField(default=False)

    def __str__(self):
        return self.nazwa

    def suma_wplat(self):
        return self.wplaty.aggregate(Sum('kwota'))['kwota__sum'] or 0

    def procent(self):
        suma = self.suma_wplat()
        if self.kwota_docelowa > 0:
            return min(int((suma / self.kwota_docelowa) * 100), 100)
        return 0

class Wplata(models.Model):
    cel = models.ForeignKey(Cel, on_delete=models.CASCADE, related_name='wplaty')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    opis = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.kwota} zł - {self.data}"