"""snack_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from snack_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # resetear contraseña
    path('api/password_reset/',
         include('django_rest_passwordreset.urls',
                 namespace='password_reset')),

    # apps locales
    re_path('', include('applications.users.urls')),
    re_path('', include('applications.events.urls')),
    re_path('', include('applications.orders.urls')),
    re_path('', include('applications.payments.urls')),

    # urls para ckeditor
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # routers
    re_path('', include('applications.events.routers')),
    re_path('', include('applications.orders.routers')),

    # Social Login
    #path("logina/", views.login, name="login"),
    #path('oauth/', include('social_django.urls', namespace='social')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
