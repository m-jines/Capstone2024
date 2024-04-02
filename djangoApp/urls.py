from django.urls import path, include
from .import views
from.views import serve_presigned_media
urlpatterns = [
        path('media/<path:file_key>/', serve_presigned_media, name='serve_presigned_media'),
        path('', views.home, name = 'home'),
        path('home/', views.home, name = 'home'),
        path('trainingjournal/', views.trainingjournal, name='trainingjournal'),
        path('techniquelibrary/', views.techniquelibrary, name='techniquelibrary'),
        path('loginpage/', views.loginpage, name = 'loginpage'),
        path('logoutuser/', views.logoutuser, name= 'logoutuser'),
        path('registerpage/', views.registerpage, name='registerpage'),
        path('journalform/', views.journalform, name='journalform'),
        path('techniqueform/', views.techniqueform, name='techniqueform'),
        path('updatejournal/<str:pk>/', views.updatejournal, name='updatejournal'),
        path('updatetechnique/<str:pk>/', views.updatetechnique, name='updatetechnique'),
        path('deletejournal/<str:pk>/', views.deletejournal, name='deletejournal'),
        path('deletetechnique/<str:pk>/', views.deletetechnique, name='deletetechnique'),
]

