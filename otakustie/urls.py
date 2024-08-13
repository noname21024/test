from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views
from core.sitemaps import StaticViewsSitemap, MangasSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views


sitemaps = {
    'static': StaticViewsSitemap,
    'mangas': MangasSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('register/', user_views.register, name = 'register'),
    path('logout/', user_views.logoutPage, name = 'logout'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name = 'django.contrib.sitemaps.views.sitemap'),
    path('user_papge/', user_views.user_page, name = 'user-page'),
    path('change_infor/', user_views.change_information, name = 'change-infor'),
    path('update_email/', user_views.updated_email, name = 'update-email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'password_complete.html'), name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)