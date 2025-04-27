from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from Petstagram.photos import views

urlpatterns = [
    path('add/', views.AddPhotoView.as_view(), name='photo-add'),
    path('<int:pk>/', include([
        path('', views.DetailsPhotoView.as_view(), name='photo-details'),
        path('edit/', views.EditPhotoView.as_view(), name='photo-edit'),
        path('delete/', views.photos_delete, name='photo-delete'),

    ]))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)