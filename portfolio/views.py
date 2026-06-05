from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import (
    Album,
    Publication,
    Video,
    ContactMessage,
    VisitorAnalytics,
)


def home(request):

    publications = Publication.objects.filter(
        is_published=True
    ).order_by('-created_at')

    albums = Album.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]

    videos = Video.objects.filter(
        is_published=True
    ).order_by('-created_at')[:6]

    context = {
        'publications': publications,
        'albums': albums,
        'videos': videos,
    }

    return render(
        request,
        'portfolio/home.html',
        context
    )


def publication_detail(request, publication_id):

    publication = get_object_or_404(
        Publication,
        id=publication_id
    )

    publication.views += 1

    publication.save()

    context = {
        'publication': publication
    }

    return render(
        request,
        'portfolio/publication_detail.html',
        context
    )


def album_list(request):
    albums = Album.objects.filter(
        is_published=True
    ).order_by('-created_at')
    return render(request, 'portfolio/album_list.html', {'albums': albums})


def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, is_published=True)
    videos = album.videos.filter(is_published=True)
    photos = album.photos.all()
    return render(request, 'portfolio/album_detail.html', {'album': album, 'videos': videos, 'photos': photos})


def about(request):

    return render(
        request,
        'portfolio/about.html'
    )


def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return redirect('/contact/')

    return render(
        request,
        'portfolio/contact.html'
    )


@login_required
def dashboard(request):

    today = now().date()

    seven_days_ago = today - timedelta(days=6)

    visitors_per_day = (
        VisitorAnalytics.objects
        .filter(
            visited_at__date__gte=seven_days_ago
        )
        .extra(
            {'day': "date(visited_at)"}
        )
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    popular_publications = (
        Publication.objects
        .order_by('-views')[:5]
    )

    total_visitors = VisitorAnalytics.objects.count()

    context = {
        'visitors_per_day': visitors_per_day,
        'popular_publications': popular_publications,
        'total_visitors': total_visitors,
    }

    return render(
        request,
        'portfolio/dashboard.html',
        context
    )
	
def cv(request):
    return render(
        request,
        'portfolio/cv.html'
    )

	
		
	
	
	
	
	
	
	
	