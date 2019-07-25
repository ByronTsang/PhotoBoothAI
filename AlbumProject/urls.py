"""AlbumProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth import views
from . import views

from .views import login, sample_api

from django.conf import settings
from django.conf.urls.static import static

#from django.urls import include   # Django QR code
from django.views.generic import RedirectView   # Django QR code
from qr_code import urls as qr_code_urls   # Django QR code

import capture.views

urlpatterns = [
    # Here we include resolver app urls
    url(r'^api/', include('resolver.urls')),
    path('api/login', login),
    path('api/sampleapi', sample_api),
    
    url(r'^admin/', admin.site.urls),# Address to admin site
    url(r"^$", views.HomePage.as_view(), name="home"),#Homepage : default
    url(r"^accounts/", include("accounts.urls", namespace="accounts")), #redirect to accounts urls file
    url(r"^accounts/", include("django.contrib.auth.urls")), #django package for user authentications
    url(r"^albums/",include("albums.urls", namespace="albums")),#redirect to albums urls file
    url(r"^photos/", include("photos.urls", namespace="photos")),#redirect to Photos urls file
    url(r"^capture/", include("capture.urls", namespace="capture")),#redirect to Capture urls file

    url(r"^home/$", views.LoginHome.as_view(), name="loginhome"), # Homepage : after Logging in
    url(r"^logout/$", views.LogoutHome.as_view(), name="logouthome"), # after Logout View

    url(r'^qrcode/(.+)$', capture.views.generate_qrcode, name='qrcode'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #for media files: albumCover and photos.

