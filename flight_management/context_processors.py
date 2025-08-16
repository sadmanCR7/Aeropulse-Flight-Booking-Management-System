# flight_management/context_processors.py
from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-sent_date')
        return {
            'unread_notifications': unread_notifications,
            'unread_count': unread_notifications.count()
        }
    return {}