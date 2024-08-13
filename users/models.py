from django.db import models
from django.contrib.auth.models import User
from core.models import Mangas, Chapters
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width > 300 or img.height > 300:
            out_size = (300, 300)
            img.thumbnail(out_size)
            img.save(self.image.path)

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    body = models.TextField(max_length=2000)
    manga = models.ForeignKey(Mangas, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now = True)
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, null = True, blank = True)

    class Meta:
        ordering = ['-created', '-updated']


    def __str__(self):
        return f"tin nhắn của {self.user.username}"

class Tes(models.Model):
    tex = models.TextField(max_length=1000)