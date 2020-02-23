from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = 'bloghome'),
    path('blogpost/<int:id>', views.blogpost, name = 'blogpost')
]
