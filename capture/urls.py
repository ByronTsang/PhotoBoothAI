from django.urls import path
from django.conf.urls import url
from . import views

app_name='capture'

urlpatterns = [    
    url(r"^$", views.CapturePhotos.as_view(), name="home"),
    #path('js/',views.index, name='index'),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.CapturePhotoDetail.as_view(),name="single"),
    url(r"new/$", views.CapturePhotos.as_view(), name="create"),
    
    #path('email/', views.EmailView, name='email'),
    #path('success/', views.SuccessView, name='success'),
    ]