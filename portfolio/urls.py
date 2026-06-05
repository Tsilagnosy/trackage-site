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
    react_publication,
)

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('albums/', album_list, name='album_list'),
    path('albums/<slug:slug>/', album_detail, name='album_detail'),
    path('contact/', contact, name='contact'),
    path('publication/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('publication/<int:publication_id>/react/', react_publication, name='react_publication'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cv/', cv, name='cv'),
]
	
	
	
	
	
	
	
	
	
	