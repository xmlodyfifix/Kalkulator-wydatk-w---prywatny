from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.lista_wydatkow, name='lista'),
    path('dodaj/', views.dodaj_wydatek, name='dodaj'),
    path('edytuj/<int:pk>/', views.edytuj_wydatek, name='edytuj'),
    path('usun/<int:pk>/', views.usun_wydatek, name='usun'),
]