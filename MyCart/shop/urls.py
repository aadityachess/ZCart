from . import views
from django.urls import path

urlpatterns = [
    path('', views.index,name='shophome'),
    path('about/', views.about,name='about'),
    path('search/', views.search,name='search'),
    path('contact/', views.contact,name='contact'),
    path('tracker/', views.tracker,name='tracker'),
    path('products/<int:myid>', views.prodview,name='prodview'),
    path('checkout/', views.checkout,name='checkout'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]
