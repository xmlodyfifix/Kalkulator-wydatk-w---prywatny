from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('logowanie/', views.logowanie, name='logowanie'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('wylogowanie/', views.wylogowanie, name='wylogowanie'),
    path('wydatki/', views.lista_wydatkow, name='lista'),
    path('wydatki/dodaj/', views.dodaj_wydatek, name='dodaj'),
    path('wydatki/edytuj/<int:pk>/', views.edytuj_wydatek, name='edytuj'),
    path('wydatki/usun/<int:pk>/', views.usun_wydatek, name='usun'),
    path('przychody/', views.lista_przychodow, name='przychody'),
    path('przychody/dodaj/', views.dodaj_przychod, name='dodaj_przychod'),
    path('przychody/edytuj/<int:pk>/', views.edytuj_przychod, name='edytuj_przychod'),
    path('przychody/usun/<int:pk>/', views.usun_przychod, name='usun_przychod'),
    path('statystyki/', views.statystyki, name='statystyki'),
    path('cele/dodaj/', views.dodaj_cel, name='dodaj_cel'),
    path('cele/edytuj/<int:pk>/', views.edytuj_cel, name='edytuj_cel'),
    path('cele/usun/<int:pk>/', views.usun_cel, name='usun_cel'),
]