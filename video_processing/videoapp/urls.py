from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='video_list'),  # List of uploaded videos
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),

    path('upload/', views.upload_video, name='upload_video'),  # Video upload form
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # Video detail with subtitles
    path('video/<int:video_id>/search/', views.search_subtitle, name='search_subtitle'),  # Search subtitle within video
]
