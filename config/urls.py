"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

# 다른 폴더내에 생성되어있는 내역을 가져오기 위해서 inclue 를 추가로 import
from django.urls import path, include

# 직접적으로 settings를 가져오는게 아니라
# settings의 mirror를 가져오는 것
# 개발단계에서만?(파일업로드 관련)
from django.conf import settings

# DEBUG 모드일때 URL 패턴을 지원해주는 module
from django.conf.urls.static import static

urlpatterns = [
    # 하기와 같은 방식으로 각 url 셋팅 가능
    # namespace를 넣는 이유는
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # MEDIA_URL이 MEDIA_ROOT로 redirect 되도록 지정
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
