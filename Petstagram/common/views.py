from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from pyperclip import copy

from django.shortcuts import render, redirect, resolve_url

from Petstagram.common.forms import CommentBaseForm, SearchForm
from Petstagram.common.models import Like
from Petstagram.photos.models import Photo


# Create your views here.

class HomePageView(ListView):
    model = Photo
    template_name = 'common/home-page.html'
    context_object_name = 'all_photos'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentBaseForm
        context['search_form'] = SearchForm(self.request.GET)

        user = self.request.user

        for photo in context['all_photos']:
            photo.has_liked = photo.like_set.filter(user=user).exists() if user.is_authenticated else False

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            queryset = queryset.filter(
                tagged_pets__name__icontains=pet_name,
            )

        return queryset


@login_required
def like_functionality(request, photo_id):
    liked_objects = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

    if liked_objects:
        liked_objects.delete()

    else:
        like = Like(to_photo_id=photo_id, user=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


@login_required
def comment_functionality(request, photo_id):
    if request.POST:
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentBaseForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
