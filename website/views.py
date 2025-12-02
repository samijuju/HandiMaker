from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Atelier, Realisation

def home(request):
    ateliers = Atelier.objects.filter(date_debut__gte=timezone.now())[:3]
    return render(request, 'website/home.html', {'ateliers': ateliers})

def boutique(request):
    objets = Realisation.objects.filter(disponible=True)
    return render(request, 'website/boutique.html', {'objets': objets})

@login_required
def inscription_atelier(request, atelier_id):
    atelier = get_object_or_404(Atelier, id=atelier_id)
    if request.user in atelier.participants.all():
        messages.info(request, "Vous êtes déjà inscrit !")
    elif atelier.places_restantes() > 0:
        atelier.participants.add(request.user)
        messages.success(request, "Inscription validée ! Handi le dodo vert est content.")
    else:
        messages.error(request, "Atelier complet.")
    return redirect('home')
