from django.urls import path

from .views import (
    home,
    about,
    contact,
    publication_detail,
    dashboard,
    cv,
)

urlpatterns = [
    path('', home, name='home'),

    path('about/', about, name='about'),

    path('contact/', contact, name='contact'),
    path('publication/<int:publication_id>/', publication_detail, name='publication_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cv/', cv, name='cv'),
]
	
	
	
	
	
	
	
	
	
	