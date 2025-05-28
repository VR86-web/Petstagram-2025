from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from Petstagram.common.forms import CommentBaseForm
from Petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from Petstagram.photos.models import Photo


# Create your views here.

class AddPhotoView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'photos/photo-add-page.html'
    form_class = PhotoAddForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()

        form.save_m2m()

        return super().form_valid(form)


class DetailsPhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photos/photo-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentBaseForm
        context['likes'] = self.object.like_set.all()
        context['comments'] = self.object.comment_set.all()
        self.object.has_liked = self.object.like_set.filter(user=self.request.user).exists()

        return context


class EditPhotoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def test_funk(self):
        photo = get_object_or_404(Photo, pk=self.kwargs['pk'])
        return self.request.user == photo.user

    def get_success_url(self):
        return redirect('photo-details', kwargs={'pk': self.object.pk})


@login_required
def photos_delete(request, pk):
    photo = Photo.objects.get(pk=pk)

    if request.user == photo.user:
        photo.delete()
    return redirect('home')

