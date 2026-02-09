from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import RedirectView
from core.views import home,no_permission

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view( url='/tasks/event_manage/',permanent=False)),
    
    path("tasks/",include("tasks.urls")),
    path("users/",include("users.urls")),
    path("no-permission/",no_permission,name='no-permission'),
    path("",home,name='home')
]+debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)