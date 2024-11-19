from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import MoveForm
from .models import Slug, Equipement

def slug_list(request):
    slugs = Slug.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'slugmonsters/slug_list.html', {"slugs": slugs, "equipements": equipements})

def slug_detail(request, id_slug):
    slug = get_object_or_404(Slug, id_slug=id_slug)
    equipements = Equipement.objects.all()
    centre = get_object_or_404(Equipement, id_equip='centre')
    arene = get_object_or_404(Equipement, id_equip='arene')
    capsule = get_object_or_404(Equipement, id_equip='capsule')
    blaster = get_object_or_404(Equipement, id_equip='blaster')
    formerlieu = get_object_or_404(Equipement, id_equip=slug.lieu.id_equip)

    if request.method == "POST":
        form = MoveForm(request.POST, instance=slug)
        if form.is_valid():
            new_lieu = form.cleaned_data['lieu']
            
            if new_lieu == formerlieu:
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"{slug} est déja dans {new_lieu}!", 'equipements': equipements, 'form': form})
            
            if new_lieu.disponibilite == 'occupe' and new_lieu != blaster:
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"Impossible, {new_lieu} est déja occupé!", 'equipements': equipements, 'form': form})
            
            if new_lieu.id_equip == 'centre' and slug.etat != 'blesse':
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"{slug} n'a pas besoin de soin!", 'equipements': equipements, 'form': form})
            
            if new_lieu.id_equip == 'arene' and slug.etat != 'pret à se battre':
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"{slug} n'est pas prêt a se battre!", 'equipements': equipements, 'form': form})
            
            if new_lieu.id_equip == 'capsule' and slug.etat != 'a besoin de dormir':
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"{slug} n'a pas besoin de dormir!", 'equipements': equipements, 'form': form})
            
            if new_lieu.id_equip == 'blaster' and slug.etat != 'endormi':
                return render(request, "slugmonsters/slug_detail.html", {'slug': slug, 'message': f"{slug} n'est pas endormi!", 'equipements': equipements, 'form': form})

            # Mise à jour de l'ancien lieu
            formerlieu.disponibilite = "libre"
            formerlieu.save()

            # Mise à jour du nouveau lieu
            new_lieu.disponibilite = "occupe"
            new_lieu.save()

            # Mise à jour de l'état du slug
            if new_lieu.id_equip == 'centre':
                slug.etat = 'a besoin de dormir'
            elif new_lieu.id_equip == 'arene':
                slug.etat = 'blesse'
            elif new_lieu.id_equip == 'capsule':
                slug.etat = 'endormi'
            elif new_lieu.id_equip == 'blaster':
                slug.etat = 'pret à se battre'

            slug.lieu = new_lieu
            slug.save()
            return redirect('slug_list')
    else:
        form = MoveForm(instance=slug)

    return render(request, 'slugmonsters/slug_detail.html', {'slug': slug, 'lieu': slug.lieu, 'form': form, 'equipements': equipements})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    slugs = Slug.objects.filter(lieu=equipement)
    if slugs.exists():
        return render(request, 'slugmonsters/equipement_detail.html', {"equipement": equipement, "slug": slugs.first()})
    else:
        if equipement.id_equip == 'blaster':
            equipement.disponibilite = 'libre'
            equipement.save()
        return render(request, 'slugmonsters/equipement_detail.html', {"equipement": equipement})
    
    
    
    
    
    
def index(request):
    # Récupérez l'état de lecture depuis la session ou initialisez-le
    audio_state = request.session.get('audio_state', {
        'is_playing': False,
        'current_time': 0,
        'volume': 0.2
    })
    return render(request, 'index.html', {'audio_state': audio_state})

def update_audio_state(request):
    if request.method == 'POST':
        # Mettez à jour l'état de lecture dans la session
        request.session['audio_state'] = {
            'is_playing': request.POST.get('is_playing') == 'true',
            'current_time': float(request.POST.get('current_time', 0)),
            'volume': float(request.POST.get('volume', 0.5))
        }
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)