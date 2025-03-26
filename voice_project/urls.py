from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from voice_agent.views import VoiceChatPage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("voice/", include("voice_agent.urls")),
    path("", VoiceChatPage.as_view(), name="voice_chat"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)