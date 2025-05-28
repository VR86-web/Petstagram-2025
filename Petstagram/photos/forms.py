from django import forms

from Petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['user',]


class PhotoAddForm(PhotoBaseForm):
    pass


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['photo',]


class PhotoDeleteForm(PhotoBaseForm):
    pass
