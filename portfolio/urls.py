from django.urls import path

from .views import (
    album_detail,
    album_list,
    about,
    contact,
    cv,
    dashboard,
    home,
    publication_detail,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('albums/', album_list, name='album_list'),
    path('albums/<slug:slug>/', album_detail, name='album_detail'),
    path('contact/', contact, name='contact'),
    path('publication/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cv/', cv, name='cv'),
]
	
	
	
	
	
	
	
	
	
	