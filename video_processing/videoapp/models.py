from django.db import models

class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.TextField()
