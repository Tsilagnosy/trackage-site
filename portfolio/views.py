from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import (
    Album,
    Publication,
    PublicationReaction,
    Video,
    VideoReaction,
    ContactMessage,
    VisitorAnalytics,
)

from django.http import JsonResponse
import uuid


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

    visitor_id = request.COOKIES.get('visitor_id')
    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    publication_ids = [pub.id for pub in publications]
    reaction_counts = PublicationReaction.objects.filter(
        publication_id__in=publication_ids
    ).values('publication_id', 'kind').annotate(count=Count('id'))

    reaction_summary_by_publication = {}
    for item in reaction_counts:
        pub_id = item['publication_id']
        kind = item['kind']
        reaction_summary_by_publication.setdefault(pub_id, {})[kind] = item['count']

    user_reactions = PublicationReaction.objects.filter(
        publication_id__in=publication_ids,
        visitor_id=visitor_id
    )
    user_reaction_by_publication = {r.publication_id: r.kind for r in user_reactions}

    video_ids = [video.id for video in videos]
    video_reaction_counts = VideoReaction.objects.filter(
        video_id__in=video_ids
    ).values('video_id', 'kind').annotate(count=Count('id'))

    reaction_summary_by_video = {}
    for item in video_reaction_counts:
        video_id = item['video_id']
        kind = item['kind']
        reaction_summary_by_video.setdefault(video_id, {})[kind] = item['count']

    video_user_reactions = VideoReaction.objects.filter(
        video_id__in=video_ids,
        visitor_id=visitor_id
    )
    user_reaction_by_video = {r.video_id: r.kind for r in video_user_reactions}

    context = {
        'publications': publications,
        'albums': albums,
        'videos': videos,
        'reaction_summary_by_publication': reaction_summary_by_publication,
        'user_reaction_by_publication': user_reaction_by_publication,
        'reaction_summary_by_video': reaction_summary_by_video,
        'user_reaction_by_video': user_reaction_by_video,
        'reaction_choices': PublicationReaction.REACTION_CHOICES,
    }

    response = render(
        request,
        'portfolio/home.html',
        context
    )
    if not request.COOKIES.get('visitor_id'):
        response.set_cookie('visitor_id', visitor_id, max_age=60*60*24*365)

    return response


def publication_detail(request, publication_id):

    publication = get_object_or_404(
        Publication,
        id=publication_id
    )
    # normal GET view: increment views and show reactions summary
    publication.views += 1
    publication.save()

    # reaction counts by kind
    reaction_counts = publication.reactions.values('kind').annotate(count=Count('id'))
    reaction_summary = {r['kind']: r['count'] for r in reaction_counts}

    # identify visitor by cookie if available, otherwise fallback to IP
    visitor_id = request.COOKIES.get('visitor_id')
    if not visitor_id:
        visitor_id = str(uuid.uuid4())

    # current visitor reaction (by visitor_id then ip)
    user_reaction = None
    if visitor_id:
        user_reaction = publication.reactions.filter(visitor_id=visitor_id).first()
    if not user_reaction:
        ip_address = request.META.get('REMOTE_ADDR')
        user_reaction = publication.reactions.filter(ip_address=ip_address).first()

    user_kind = user_reaction.kind if user_reaction else None

    context = {
        'publication': publication,
        'reaction_summary': reaction_summary,
        'user_reaction_kind': user_kind,
    }

    response = render(
        request,
        'portfolio/publication_detail.html',
        context
    )

    # ensure visitor_id cookie is set for future requests
    if not request.COOKIES.get('visitor_id'):
        response.set_cookie('visitor_id', visitor_id, max_age=60*60*24*365)  # 1 year

    return response


def react_publication(request, publication_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    publication = get_object_or_404(Publication, id=publication_id)
    kind = request.POST.get('kind') or request.JSON.get('kind') if hasattr(request, 'JSON') else request.POST.get('kind')
    if kind not in dict(PublicationReaction.REACTION_CHOICES):
        return JsonResponse({'error': 'Invalid reaction kind'}, status=400)

    visitor_id = request.COOKIES.get('visitor_id')
    ip_address = request.META.get('REMOTE_ADDR')
    lookup_kwargs = {'publication': publication}
    if visitor_id:
        lookup_kwargs['visitor_id'] = visitor_id
    else:
        lookup_kwargs['ip_address'] = ip_address

    existing = PublicationReaction.objects.filter(**lookup_kwargs).first()
    active = True
    if existing:
        if existing.kind == kind:
            existing.delete()
            active = False
        else:
            existing.kind = kind
            existing.save(update_fields=['kind'])
            active = True
    else:
        PublicationReaction.objects.create(publication=publication, ip_address=ip_address, visitor_id=visitor_id, kind=kind)
        active = True

    # return updated counts
    reaction_counts = publication.reactions.values('kind').annotate(count=Count('id'))
    summary = {r['kind']: r['count'] for r in reaction_counts}
    total = sum(summary.values())
    # compute stars based on total
    if total > 50:
        stars = 4
    elif 30 <= total <= 50:
        stars = 3
    else:
        stars = 2

    return JsonResponse({'summary': summary, 'total': total, 'stars': stars, 'active': active, 'selected_kind': kind})


def react_video(request, video_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    video = get_object_or_404(Video, id=video_id)
    kind = request.POST.get('kind') or request.JSON.get('kind') if hasattr(request, 'JSON') else request.POST.get('kind')
    if kind not in dict(VideoReaction.REACTION_CHOICES):
        return JsonResponse({'error': 'Invalid reaction kind'}, status=400)

    visitor_id = request.COOKIES.get('visitor_id')
    ip_address = request.META.get('REMOTE_ADDR')
    lookup_kwargs = {'video': video}
    if visitor_id:
        lookup_kwargs['visitor_id'] = visitor_id
    else:
        lookup_kwargs['ip_address'] = ip_address

    existing = VideoReaction.objects.filter(**lookup_kwargs).first()
    active = True
    if existing:
        if existing.kind == kind:
            existing.delete()
            active = False
        else:
            existing.kind = kind
            existing.save(update_fields=['kind'])
            active = True
    else:
        VideoReaction.objects.create(video=video, ip_address=ip_address, visitor_id=visitor_id, kind=kind)
        active = True

    reaction_counts = video.reactions.values('kind').annotate(count=Count('id'))
    summary = {r['kind']: r['count'] for r in reaction_counts}
    total = sum(summary.values())

    return JsonResponse({'summary': summary, 'total': total, 'active': active, 'selected_kind': kind})


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

	
		
	
	
	
	
	
	
	
	