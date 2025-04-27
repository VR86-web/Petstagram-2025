from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from Petstagram.common.forms import CommentBaseForm
from Petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from Petstagram.photos.models import Photo


# Create your views here.

class AddPhotoView(CreateView):
    model = Photo
    template_name = 'photos/photo-add-page.html'
    form_class = PhotoAddForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)


class DetailsPhotoView(DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentBaseForm
        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()

        return context


class EditPhotoView(UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self):
        return redirect('photo-details', kwargs={'pk': self.object.pk})


def photos_delete(request, pk):
    Photo.objects.get(pk=pk).delete()
    return redirect('home')

