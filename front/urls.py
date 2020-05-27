from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_file),
    path('lexical', views.lexical, name='lexical'),
    path('syntax', views.syntax, name='syntax'),
]
