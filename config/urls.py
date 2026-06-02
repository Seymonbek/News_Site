from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('app.urls')),
    path('account/', include('accounts.urls')),
)

# Media fayllar: faqat development'da Django orqali serve qilinadi.
# Production'da Nginx yoki shunga o'xshash server media fayllarni serve qiladi.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
