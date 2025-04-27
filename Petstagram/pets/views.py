from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from Petstagram.common.forms import CommentBaseForm
from Petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from Petstagram.pets.models import Pet


# Create your views here.
class AddPetView(CreateView):
    model = Pet
    form_class = PetAddForm
    template_name = 'pets/pet-add-page.html'

    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})


class PetDetailsView(DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    context_object_name = 'pet'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentBaseForm()
        context['all_photos'] = self.object.photo_set.all()

        return context


class EditPetView(UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'
    context_object_name = 'pet'

    def get_success_url(self):
        return reverse_lazy('pet-details',
                            kwargs={'username': self.kwargs['username'], 'pet_slug': self.kwargs['pet_slug']})


class DeletePetView(DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetDeleteForm
    success_url = reverse_lazy('profile-details', kwargs={'pk': 1})

    def get_initial(self):
        return self.object.__dict__

    def get_form_kwargs(self):
        kwargs = super(). get_form_kwargs()
        kwargs.update({'data': self.get_initial()})

        return kwargs
