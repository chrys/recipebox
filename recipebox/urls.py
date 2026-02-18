from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Everything lives under /recipes/ — one nginx location block, no conflicts
    path('recipes/admin/', admin.site.urls),
    path('recipes/accounts/', include('accounts.urls')),
    path('recipes/calendar/', include('calendar_app.urls')),
    path('recipes/', include('recipes.urls')),
    # Root redirect so hitting / sends the user somewhere sensible
    path('', RedirectView.as_view(url='/recipes/', permanent=False)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
