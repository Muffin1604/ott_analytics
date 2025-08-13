from django.shortcuts import render
from django.db.models import Sum, Avg, Count, F, Q
from django.db.models.functions import TruncHour
from django.utils import timezone
from datetime import timedelta
from .models import User, Video, WatchSession
import json

def home(request):
    return render(request, 'analytics/home.html')

def general_dashboard(request):
    end = timezone.now()
    start = end - timedelta(days=7)
    trending = (WatchSession.objects
                .filter(start_time__range=(start, end))
                .values('video__title')
                .annotate(views=Count('id'))
                .order_by('-views')[:10])
    active_users = (User.objects
                    .annotate(total_watch=Sum('sessions__session_duration'))
                    .order_by('-total_watch')[:10])
    genre_trends = (WatchSession.objects
                    .filter(start_time__range=(start, end))
                    .values(genre=F('video__genre'))
                    .annotate(total_watch=Sum('session_duration'))
                    .order_by('-total_watch'))
    heatmap_qs = (WatchSession.objects
               .filter(start_time__range=(start, end))
               .annotate(hour=TruncHour('start_time'))
               .values('hour')
               .annotate(total_watch=Sum('session_duration'))
               .order_by('hour'))
    heatmap = [{'hour': h['hour'].strftime('%Y-%m-%d %H:%M:%S'), 'total_watch': h['total_watch']} for h in heatmap_qs]
    genre_labels = [item['genre'] for item in genre_trends]
    genre_data = [item['total_watch'] for item in genre_trends]

    heat_labels = [item['hour'] for item in heatmap]
    heat_data = [item['total_watch'] for item in heatmap]

    context = {
        'genre_labels': json.dumps(genre_labels),
        'genre_data': json.dumps(genre_data),
        'heat_labels': json.dumps(heat_labels),
        'heat_data': json.dumps(heat_data),
        'active_users' : active_users,
        'trending': trending
    }
    return render(request, 'analytics/general_dashboard.html', context)

def user_analytics(request):
    total_watch = WatchSession.objects.aggregate(total=Sum('session_duration'))['total'] or 0
    top_genres = (WatchSession.objects
                  .values('video__genre')
                  .annotate(total_watch=Sum('session_duration'))
                  .order_by('-total_watch')[:10])
    top_videos = (WatchSession.objects
                  .values('video__title')
                  .annotate(views=Count('id'), avg_watch=Avg('session_duration'))
                  .order_by('-views')[:10])
    avg_session = WatchSession.objects.aggregate(avg=Avg('session_duration'))['avg'] or 0
    device_usage = (WatchSession.objects
                    .values('device_type')
                    .annotate(count=Count('id')))
    # Prepare lists for charts
    device_labels = [d['device_type'] for d in device_usage]
    device_counts = [d['count'] for d in device_usage]
    return render(request, 'analytics/user_analytics.html', {
        'total_watch': total_watch,
        'top_genres': list(top_genres),
        'top_videos': list(top_videos),
        'avg_session': avg_session,
        'device_usage': list(device_usage),
        'device_labels': device_labels,
        'device_counts': device_counts
    })

def video_analytics(request):
    videos = (Video.objects
              .annotate(total_views=Count('sessions'),
                        avg_watch=Avg('sessions__session_duration'),
                        rewatch_count=Count('sessions', filter=Q(sessions__is_rewatch=True)))
              .order_by('-total_views'))
    return render(request, 'analytics/video_analytics.html', {'videos': videos})
