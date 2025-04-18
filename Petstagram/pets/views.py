from django.shortcuts import render, redirect

from Petstagram.common.forms import CommentBaseForm
from Petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from Petstagram.pets.models import Pet


# Create your views here.


def pets_add(request):
    form = PetAddForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('profile-details', pk=1)

    context = {
        'form': form,
    }
    return render(request, 'pets/pet-add-page.html', context)


def pets_details(request, username, pet_slug):

    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()
    comment_form = CommentBaseForm()

    context = {
        'pet': pet,
        'all_photos': all_photos,
        'comment_form': comment_form,
    }

    return render(request, 'pets/pet-details-page.html', context)


def pets_edit(request, username, slug):
    pet = Pet.objects.get(slug=slug)
    form = PetEditForm(request.POST or None, instance=pet)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('pet-details', username, slug)

    context = {
        'form': form,
        'pet': pet,
    }

    return render(request, 'pets/pet-edit-page.html', context)


def pets_delete(request, username, slug):
    pet = Pet.objects.get(slug=slug)
    form = PetDeleteForm(instance=pet)

    if request.method == 'POST':
        pet.delete()
        return redirect('profile-details', pk=1)

    context = {
        'pet': pet,
        'form': form
    }

    return render(request, 'pets/pet-delete-page.html', context)

