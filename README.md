# BudżetApp

Prywatna aplikacja do śledzenia wydatków i przychodów domowych, zrobiona w Django.

## Funkcjonalności
- logowanie i rejestracja (osobne konta)
- dodawanie wydatków i przychodów
- filtrowanie po kategorii
- widok wspólny i prywatny
- cele oszczędnościowe z paskiem postępu
- wykres wydatków per kategoria
- statystyki miesięczne

## Uruchomienie

Zainstaluj wymagane paczki:
```bash
pip install django
pip install django-filter
```

Uruchom serwer:
```bash
python manage.py migrate
python manage.py runserver
```

Aplikacja działa pod adresem http://127.0.0.1:8000
