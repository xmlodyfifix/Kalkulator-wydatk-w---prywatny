from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Wydatek, Przychod, Cel, Wplata
from .forms import WydatekForm, PrzychodzForm, CelForm, WydatekFilter, WplataForm
import json

def rejestracja(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Rejestracja'})

def logowanie(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Logowanie'})

def wylogowanie(request):
    logout(request)
    return redirect('logowanie')

@login_required
def dashboard(request):
    pokaz = request.GET.get('pokaz', 'moje')

    if pokaz == 'wspolne':
        wydatki_qs = Wydatek.objects.filter(wspolne=True)
        przychody_qs = Przychod.objects.filter(wspolne=True)
        cele = Cel.objects.filter(wspolne=True)
    else:
        wydatki_qs = Wydatek.objects.filter(user=request.user)
        przychody_qs = Przychod.objects.filter(user=request.user)
        cele = Cel.objects.filter(user=request.user)

    total_wydatki = wydatki_qs.aggregate(Sum('kwota'))['kwota__sum'] or 0
    total_przychody = przychody_qs.aggregate(Sum('kwota'))['kwota__sum'] or 0
    saldo = total_przychody - total_wydatki

    sumy_kategorii = wydatki_qs.values('kategoria').annotate(suma=Sum('kwota'))
    labels = [s['kategoria'] for s in sumy_kategorii]
    values = [float(s['suma']) for s in sumy_kategorii]

    ostatnie_wydatki = wydatki_qs.order_by('-data')[:5]

    return render(request, 'tracker/dashboard.html', {
        'total_wydatki': total_wydatki,
        'total_przychody': total_przychody,
        'saldo': saldo,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
        'ostatnie_wydatki': ostatnie_wydatki,
        'cele': cele,
        'pokaz': pokaz,
    })

@login_required
def lista_wydatkow(request):
    pokaz = request.GET.get('pokaz', 'moje')
    if pokaz == 'wspolne':
        wydatki = Wydatek.objects.filter(wspolne=True).order_by('-data')
    else:
        wydatki = Wydatek.objects.filter(user=request.user).order_by('-data')
    f = WydatekFilter(request.GET, queryset=wydatki)
    sumy = f.qs.values('kategoria').annotate(suma=Sum('kwota')).order_by('kategoria')
    return render(request, 'tracker/lista.html', {'filter': f, 'sumy': sumy, 'pokaz': pokaz})

@login_required
def dodaj_wydatek(request):
    if request.method == 'POST':
        form = WydatekForm(request.POST)
        if form.is_valid():
            wydatek = form.save(commit=False)
            wydatek.user = request.user
            wydatek.save()
            return redirect('lista')
    else:
        form = WydatekForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Dodaj wydatek'})

@login_required
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

@login_required
def usun_wydatek(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    if request.method == 'POST':
        wydatek.delete()
        return redirect('lista')
    return render(request, 'tracker/usun.html', {'wydatek': wydatek})

@login_required
def lista_przychodow(request):
    pokaz = request.GET.get('pokaz', 'moje')
    if pokaz == 'wspolne':
        przychody = Przychod.objects.filter(wspolne=True).order_by('-data')
    else:
        przychody = Przychod.objects.filter(user=request.user).order_by('-data')
    return render(request, 'tracker/przychody.html', {'przychody': przychody, 'pokaz': pokaz})

@login_required
def dodaj_przychod(request):
    if request.method == 'POST':
        form = PrzychodzForm(request.POST)
        if form.is_valid():
            przychod = form.save(commit=False)
            przychod.user = request.user
            przychod.save()
            return redirect('przychody')
    else:
        form = PrzychodzForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Dodaj przychód'})

@login_required
def edytuj_przychod(request, pk):
    przychod = get_object_or_404(Przychod, pk=pk)
    if request.method == 'POST':
        form = PrzychodzForm(request.POST, instance=przychod)
        if form.is_valid():
            form.save()
            return redirect('przychody')
    else:
        form = PrzychodzForm(instance=przychod)
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Edytuj przychód'})

@login_required
def usun_przychod(request, pk):
    przychod = get_object_or_404(Przychod, pk=pk)
    if request.method == 'POST':
        przychod.delete()
        return redirect('przychody')
    return render(request, 'tracker/usun.html', {'wydatek': przychod})

@login_required
def statystyki(request):
    wydatki_miesiac = (
        Wydatek.objects.filter(user=request.user)
        .annotate(miesiac=TruncMonth('data'))
        .values('miesiac')
        .annotate(suma=Sum('kwota'))
        .order_by('miesiac')
    )
    przychody_miesiac = (
        Przychod.objects.filter(user=request.user)
        .annotate(miesiac=TruncMonth('data'))
        .values('miesiac')
        .annotate(suma=Sum('kwota'))
        .order_by('miesiac')
    )

    labels = [w['miesiac'].strftime('%B %Y') for w in wydatki_miesiac]
    wydatki_values = [float(w['suma']) for w in wydatki_miesiac]
    przychody_dict = {p['miesiac']: float(p['suma']) for p in przychody_miesiac}
    przychody_values = [przychody_dict.get(w['miesiac'], 0) for w in wydatki_miesiac]

    return render(request, 'tracker/statystyki.html', {
        'labels': json.dumps(labels),
        'wydatki_values': json.dumps(wydatki_values),
        'przychody_values': json.dumps(przychody_values),
    })

@login_required
def dodaj_cel(request):
    if request.method == 'POST':
        form = CelForm(request.POST)
        if form.is_valid():
            cel = form.save(commit=False)
            cel.user = request.user
            cel.save()
            return redirect('dashboard')
    else:
        form = CelForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Dodaj cel'})

@login_required
def edytuj_cel(request, pk):
    cel = get_object_or_404(Cel, pk=pk)
    if request.method == 'POST':
        form = CelForm(request.POST, instance=cel)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CelForm(instance=cel)
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': 'Edytuj cel'})

@login_required
def usun_cel(request, pk):
    cel = get_object_or_404(Cel, pk=pk)
    if request.method == 'POST':
        cel.delete()
        return redirect('dashboard')
    return render(request, 'tracker/usun.html', {'wydatek': cel})

@login_required
def szczegoly_celu(request, pk):
    cel = get_object_or_404(Cel, pk=pk)
    wplaty = cel.wplaty.all().order_by('-data')
    suma = cel.suma_wplat()
    pozostalo = cel.kwota_docelowa - suma
    return render(request, 'tracker/cel_szczegoly.html', {
        'cel': cel,
        'wplaty': wplaty,
        'suma': suma,
        'pozostalo': pozostalo,
    })

@login_required
def dodaj_wplate(request, pk):
    cel = get_object_or_404(Cel, pk=pk)
    if request.method == 'POST':
        form = WplataForm(request.POST)
        if form.is_valid():
            wplata = form.save(commit=False)
            wplata.cel = cel
            wplata.user = request.user
            wplata.save()
            return redirect('szczegoly_celu', pk=pk)
    else:
        form = WplataForm()
    return render(request, 'tracker/formularz.html', {'form': form, 'tytul': f'Dodaj wpłatę do: {cel.nazwa}'})

@login_required
def usun_wplate(request, pk):
    wplata = get_object_or_404(Wplata, pk=pk)
    cel_pk = wplata.cel.pk
    if request.method == 'POST':
        wplata.delete()
        return redirect('szczegoly_celu', pk=cel_pk)
    return render(request, 'tracker/usun.html', {'wydatek': wplata})