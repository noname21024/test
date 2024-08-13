from django.shortcuts import render, redirect
from .models import Images, Mangas, Chapters, Tags, HistoryWatch, Following
import json
from django.db.models import Q
from django.core.paginator import Paginator
from .form import MangaForm
from django.template.defaulttags import register
from functools import reduce
import operator
from users.models import Messages



@register.filter(name='split')
def split(value, key): 
 
    value.split("key")
    return value.split(key)


def get_json_file():
    list = []
    #  page 11 12 16 
    # đã load trang 20 từ trang 11 
    
    with open(f'Chuyển sinh thành kết giới sư.json', 'r', encoding='utf-8') as f:
        for data in json.load(f):
            if data['name'] != None:
                list.append(data)

    return list


def home(request):
    images = Images.objects.all()
    tags = Tags.objects.all()

    # logic ở đay là tạo luôn cả chapter


    # data = get_json_file()

    # for item in data:
    #     try:
    #         for tag in item['tags']:
    #             Tags.objects.get_or_create(name = tag)
    #     except:
    #         pass
        
    #     if Mangas.objects.filter(name = item['name']):
    #         current_manga = Mangas.objects.get(name = item['name'])
    #         if current_manga.name == item['name']:
    #             try:
    #                 for tag in item['tags']:
    #                     category = Tags.objects.get(name = tag)
    #                     current_manga.tags.add(category)
    #             except:
    #                 pass
    #             try:
    #                 for chapter in item['chapter']:
    #                     name, value = get_chapter(chapter)
    #                     current_chapter = Chapters.objects.filter(manga = current_manga, chaptername = name)
    #                     if current_chapter:
    #                         name_of_chapter = get_images(current_chapter)
    #                         get_chap = Chapters.objects.get(manga = current_manga, chaptername = name_of_chapter)
    #                         try:
    #                             for img in value:
    #                                     image = Images.objects.get_or_create(manga = current_manga, chapters = get_chap, image = img)
    #                                     if image[0].image == value[-1]:
    #                                         break
    #                         except:
    #                             pass
    #                     else:
    #                         Chapters.objects.create(manga = current_manga, chaptername = name)
    #             except:
    #                 pass
    #     else:
    #         Mangas.objects.create(name = item['name'], description = "Chưa có descriptions cho bộ truyện này", image = item['image'])

# #  item['description']

    mangas = Mangas.objects.all()

    top_manga = mangas.order_by('-all_views')

    paginator = Paginator(mangas, 36)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'images': images,
        'mangas': mangas, 
        'tags': tags,
        'page': page,
        'manga_ratings': mangas,
        'top_mangas': top_manga,
    }
    return render(request, 'home.html', context)

def list_manga(request, pk):
    images = Images.objects.all()
    tags = Tags.objects.all()
    category = ''

# query = reduce(operator.and_, (Q(group__id=group_id) for group_id in group_ids))

# persons_qs = Person.objects.exclude(~query)
    
    # if request.method == 'POST':
    #     list = request.POST.getlist('filter-tag')
    #     mangas = Mangas.objects.filter(reduce(operator.and_, [Q(tags__name=c) for c in list]))

    # action = Tags.objects.get(name = 'Action')
    # fantasy = Tags.objects.get(name = 'Drama')
    
    # mangas = Mangas.objects.all().filter_all_many_to_many('tags', action, fantasy)

    if pk != 'None':
        mangas = Mangas.objects.filter(Q(tags__pk = int(pk)))
        category = Tags.objects.get(id = pk).name

    else:
        mangas = Mangas.objects.all()
        category = ''

    paginator = Paginator(mangas, 36)
    page = paginator.get_page(request.GET.get('page'))
    context = {
        'images': images,
        'mangas': mangas, 
        'tags': tags,
        'page': page,
        'index': pk,
        'category': category
    }
    
    return render(request, 'list.html', context)

def get_chapter(obj):
    for key, value in obj.items():
        return key, value
    
def get_images(chapter):
    for chapter in chapter:
        return chapter.chaptername


def manga_content(request, name, pk):
    manga = Mangas.objects.get(name = name)
    chapter = Chapters.objects.get(manga = manga, id = pk)
    images = chapter.images.all()

    chapter.views += 1
    chapter.save()

    if request.method == 'POST':
        action = request.POST.get('follow')
        if action == 'follow':
            Following.objects.get_or_create(manga = manga, user = request.user)
        elif action == 'unfollow':
            Following.objects.get(manga = manga, user = request.user).delete()  
            
    try:
        following = request.user.follows.get(manga = manga)
    except:
        following = None

    try:    
        obj = HistoryWatch.objects.filter(manga = manga, user = request.user).first()
        if obj != None:
            obj.chapter = chapter
            obj.save()
        else:
            HistoryWatch.objects.create(manga = manga, user = request.user, chapter = chapter)
    except:
        pass

    context = {
        'images': images,
        'manga': manga,
        'chapternum': chapter.chaptername,
        'chap': 'chap',
        'tags': Tags.objects.all(),
        'current_chapter': chapter,
        'following': following,
        'title': manga.name,
    }

    return render(request, 'content.html', context)

def room(request, title):
    manga = Mangas.objects.get(name = title)
    tags = Tags.objects.all()
    continue_read = None


    try:
        history = HistoryWatch.objects.filter(manga = manga, user = request.user).first()
        continue_read = history.chapter
    except:
        pass

    if request.method == 'POST':
        action = request.POST.get('follow')
        if action == 'follow':
            Following.objects.get_or_create(manga = manga, user = request.user)
        elif action == 'unfollow':
            Following.objects.get(manga = manga, user = request.user).delete()  
        
        elif action == 'message':
            Messages.objects.get_or_create(user = request.user, body = request.POST.get('message'), manga = manga)
        elif action == 'delete-message':
            try:
                id = request.POST.get('message-id')
                Messages.objects.get(manga = manga, user = request.user, id = id).delete()
            except:
                pass
    try:
        following = request.user.follows.get(manga = manga)
    except:
        following = None
    
    chapters = manga.chapters.all()
    new = manga.chapters.first()
    last = manga.chapters.last()

    all_views = 0

    for chapter in chapters:
        all_views += chapter.views

    manga.all_views = all_views
    manga.save()
    message = Messages.objects.filter(manga = manga)

    user = False
    
    try:
        if request.user == message.all().first().user:
            user = True
        else:
            user = False
    except:
        pass

    context = {
        'manga': manga,
        'chapters': chapters,
        'tags': tags,
        'new_chapter': new,
        'last_chapter': last,
        'tags_manga': manga.tags.all(),
        'tags': tags,
        'continue_read': continue_read,
        'following': following,
        'description': manga.description,
        'title': manga.name,
        'messages': message,
        'message_user': user
    }
    return render(request, 'room.html', context)

def security_page(request):
    return render(request, 'security.html')

def nav(request):
    return render(request, 'mega.html')

def following_page(request):

    following = request.user.follows.all()
    paginator = Paginator(following, 36)
    page = paginator.get_page(request.GET.get('page'))
    tags = Tags.objects.all()

    context = {
        'page': page,
        'tags': tags,
    }

    return render(request, 'following.html', context)


def following_page_user(request):
    following = request.user.follows.all()
    paginator = Paginator(following, 36)
    page = paginator.get_page(request.GET.get('page'))
    tags = Tags.objects.all()

    context = {
        'page': page,
        'tags': tags,
    }
    return render(request, 'user_page_following.html', context)

def search_manga(request):
    manga_text = request.POST.get('q') if request.POST.get('q') != None else ''

    if manga_text != '':
        results = Mangas.objects.filter(name__icontains = manga_text)
    else:
        results = None

    context = {'results': results}

    return render(request, 'manga-results.html', context)

def manga_search_result(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    no_result = True

    if q != '':
        mangas = Mangas.objects.filter(Q(name__icontains = q))
        no_result = False
    else:
        mangas = Mangas.objects.all()

    paginator = Paginator(mangas, 36)
    page = paginator.get_page(request.GET.get('page'))

    context = {
        'page': page,
        'no_result': no_result,
        'q': q
    }

    return render(request, 'manga_result.html', context)

def history_view(request):
    history_all = request.user.histories.all()

    paginator = Paginator(history_all, 36)
    page = paginator.get_page(request.GET.get('page'))

    context = {'page': page}

    return render(request, 'history_view.html', context)

def history_user_page(request):
    history_all = request.user.histories.all()

    paginator = Paginator(history_all, 36)
    page = paginator.get_page(request.GET.get('page'))

    context = {'page': page}

    return render(request, 'history_user_page.html', context)