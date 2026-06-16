# System monitorowania wydatków domowych

## Spis treści
1. [Opis projektu](#opis-projektu)
2. [Funkcjonalności](#funkcjonalności)
3. [Instrukcja uruchomienia](#instrukcja-uruchomienia)

## Opis projektu
Projekt zaliczeniowy z przedmiotu Wzorzec MVC w tworzeniu aplikacji internetowych.
Aplikacja do zapisywania wydatków domowych zrobiona w Django.

## Funkcjonalności
- dodawanie wydatku (nazwa, kwota, kategoria, data)
- lista wszystkich wydatków
- edycja i usuwanie wydatków
- filtrowanie po kategorii
- walidacja formularzy
- podsumowanie wydatków per kategoria

## Instrukcja uruchomienia

Zainstalować wymagane paczki:
```bash
pip install django
pip install django-filter
```

Uruchomić serwer:
```bash
python manage.py migrate
python manage.py runserver
```

Aplikacja działa pod adresem http://127.0.0.1:8000
Panel admina: http://127.0.0.1:8000/admin (trzeba utworzyć konto: python manage.py createsuperuser)