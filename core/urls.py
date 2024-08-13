from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('room/<str:title>/', views.room, name = 'room'),
    path('content/<str:name>/<str:pk>/', views.manga_content, name = 'manga-content'),
    path('security_page/', views.security_page, name = 'security'),
    path('list_manga/<str:pk>/', views.list_manga, name = 'list'),
    path('following_page/', views.following_page, name = 'following-page'),
    path('search_manga', views.search_manga, name = 'search-manga'),
    path('tim_kiem/', views.manga_search_result, name = 'manga-search-result'),
    path('lich_su/', views.history_view, name = 'history_view'),
    path('following/', views.following_page_user, name = 'following-page-user'),
    path('history_user_page/', views.history_user_page, name = 'history-user-page'),

]

# 