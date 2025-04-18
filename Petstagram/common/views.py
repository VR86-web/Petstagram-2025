from pyperclip import copy

from django.shortcuts import render, redirect, resolve_url

from Petstagram.common.forms import CommentBaseForm, SearchForm
from Petstagram.common.models import Like
from Petstagram.photos.models import Photo


# Create your views here.


def home(request):
    search_form = SearchForm(request.GET)
    comment_form = CommentBaseForm()

    all_photos = Photo.objects.all()

    if search_form.is_valid():
        all_photos = all_photos.filter(
            tagged_pets__name__icontains=search_form.cleaned_data['pet_name'],
        )

    context = {
        'all_photos': all_photos,
        'comment_form': comment_form,
        'search_form': search_form,
    }

    return render(request, 'common/home-page.html', context)


def like_functionality(request, photo_id):
    liked_objects = Like.objects.filter(to_photo_id=photo_id).first()

    if liked_objects:
        liked_objects.delete()

    else:
        like = Like(to_photo_id=photo_id)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def comment_functionality(request, photo_id):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentBaseForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
