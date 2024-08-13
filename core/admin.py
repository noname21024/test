from django.contrib import admin
from .models import Images, Mangas, Chapters, Tags, Following, HistoryWatch

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']

# Register your models here.
admin.site.register(Images)
admin.site.register(Mangas, ItemAdmin)
admin.site.register(Chapters)
admin.site.register(Tags)
admin.site.register(Following)
admin.site.register(HistoryWatch)
