from django.db import models
from PIL import Image
from django.core.files import File
from urllib import request
import os
from django.contrib.auth.models import User

class Tags(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(max_length= 2000)
    def __str__(self):
        return self.name

class AllManyToManyQuerySet(models.QuerySet):
    def filter_all_many_to_many(self, attribute, *args):
        qs = self
        for arg in args:
            qs = qs.filter(**{attribute: arg})
        return qs

class Mangas(models.Model):
    name = models.CharField(max_length = 2000)
    description = models.TextField(max_length = 2000)
    image = models.URLField()
    tags = models.ManyToManyField(Tags)
    objects = AllManyToManyQuerySet.as_manager()
    all_views = models.IntegerField(default = 0)

    def get_remote_image(self):
        if self.image:
            result = request.urlretrieve(self.image)
            self.image_file.save(
                    os.path.basename(self.image),
                    File(open(result[0], 'rb'))
                    )
            self.save()
    
    def __str__(self):
        return self.name
    
class Chapters(models.Model):
    manga = models.ForeignKey(Mangas, on_delete = models.CASCADE, related_name = 'chapters')
    chaptername = models.CharField(max_length = 2000)
    views = models.IntegerField(default = 0)

    def __str__(self):
        return self.chaptername


class Images(models.Model):
    manga = models.ForeignKey(Mangas, on_delete = models.CASCADE)
    chapters = models.ForeignKey(Chapters, on_delete = models.CASCADE, related_name = "images")
    image = models.URLField()
    def get_remote_image(self):
        if self.image:
            result = request.urlretrieve(self.image)
            self.image_file.save(
                    os.path.basename(self.image),
                    File(open(result[0], 'rb'))
                    )
            self.save()

# Create your models here.
    
class HistoryWatch(models.Model):
    manga = models.ForeignKey(Mangas, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'histories')
    chapter = models.ForeignKey(Chapters, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now =True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return f'{self.manga.name} - {self.chapter.chaptername}'

class Following(models.Model):
    manga = models.ForeignKey(Mangas, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'follows')

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now =True)
    
    class Meta:
        ordering = ['-created', '-updated']