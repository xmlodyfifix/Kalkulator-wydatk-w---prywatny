from django.shortcuts import render, get_object_or_404, redirect
from .models import Wydatek
from .forms import WydatekForm, WydatekFilter
from django.db.models import Sum

def lista_wydatkow(request):
    wydatki = Wydatek.objects.all().order_by('-data')
    f = WydatekFilter(request.GET, queryset=wydatki)
    
    sumy = f.qs.values('kategoria').annotate(suma=Sum('kwota')).order_by('kategoria')
    
    return render(request, 'tracker/lista.html', {
        'filter': f,
        'sumy': sumy,
    })

def dodaj_wydatek(request):
    if request.method == 'POST':
        form = WydatekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = WydatekForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Dodaj wydatek'})

def edytuj_wydatek(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    if request.method == 'POST':
        form = WydatekForm(request.POST, instance=wydatek)
        if form.is_valid():
            form.save()
            return redirect('lista')
    else:
        form = WydatekForm(instance=wydatek)
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Edytuj wydatek'})

def usun_wydatek(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    if request.method == 'POST':
        wydatek.delete()
        return redirect('lista')
    return render(request, 'tracker/usun.html', {'wydatek': wydatek})