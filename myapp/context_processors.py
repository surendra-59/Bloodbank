from .models import HospitalNotification

def hospital_notifications(request):
    if request.user.is_authenticated and request.user.user_type == "2":
        notifications = HospitalNotification.objects.filter(hospital=request.user).order_by("-created_at")
        unread_count = notifications.filter(is_read=False).count()
        return {
            'notifications': notifications,
            'unread_notifications_count': unread_count
        }
    return {}


