from django.shortcuts import render, redirect

from Petstagram.common.forms import CommentBaseForm
from Petstagram.common.models import Like
from Petstagram.photos.forms import PhotoAddForm, PhotoEditForm
from Petstagram.photos.models import Photo


# Create your views here.


def photos_add(request):
    form = PhotoAddForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }

    return render(request, 'photos/photo-add-page.html', context)


def photos_details(request, pk):

    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.all()
    comments = photo.comment_set.all()
    comment_form = CommentBaseForm()

    context = {
        'photo': photo,
        'likes': likes,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'photos/photo-details-page.html', context)


def photos_edit(request, pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoEditForm(request.POST or None, instance=photo)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('photo-details', pk)

    context = {
        'photo': photo,
        'form': form,
    }

    return render(request, 'photos/photo-edit-page.html', context)


def photos_delete(request, pk):
    Photo.objects.get(pk=pk).delete()
    return redirect('home')

