from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from SocialSite import settings
from SocialApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Main),
    path('Explore',views.Explore,name='Explore'),
    path('Signup/',views.Signup,name='Signup'),
    path('Login/',views.Login,name='Login'),
    path('Logout/',views.Logout,name='Logout'),
    path('upload',views.upload,name='upload'),
    path('Likes/<str:id>',views.Likes,name='Likes'),
    path('#<str:id>',views.Home_post,name='Home_post'),
    path('profile/<str:id_user>',views.profile,name='profile'),
    path('Delete/<str:id>',views.Delete,name='Delete'),
    path('Search_results/',views.Search_results,name='Search_results'),
    path('Follow',views.Follow,name='Follow'),
    ]




    
 