from django.urls import path
from . import views
from django.conf.urls.static import static  
from django.conf import settings 

urlpatterns = [
    path('homepage',views.homepage,name='homepage'),
    path('predictImage',views.predictImage,name='predictImage'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('',views.index,name='index')

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)