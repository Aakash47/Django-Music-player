from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('songs/', views.songs, name = 'songs'),
    path('mysongs/', views.mysongs, name = 'mysongs'),
    path('upload-song/', views.uploadsong, name = 'uploadsong'),
    path('delete-song/<int:song_id>/', views.deletesong, name = 'deletesong'),
    path('songs/<int:id>/', views.songpost, name = 'songpost'),
    path('signup/', views.signup, name = "signup"),
    path('login/', views.loginuser, name = "login"),
    path('logout_user/', views.logout_user, name = "logout"),
    path('myplaylist/', views.watchlater, name = "watchlater"),
    path('remove/<int:watch_id>/', views.removewatchlater, name = "removewatchlater"),
    path('history/', views.history, name = "history")



] 
