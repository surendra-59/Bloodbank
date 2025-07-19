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

# from .models import HospitalNotification

# def hospital_notifications(request):
#     if request.user.is_authenticated:
#         print("User authenticated:", request.user.email)
#         print("User type:", request.user.user_type)
        
#         if str(request.user.user_type) == "2":
#             notifications = HospitalNotification.objects.filter(hospital=request.user).order_by("-created_at")
#             unread_count = notifications.filter(is_read=False).count()
#             print("Unread count:", unread_count)

#             return {
#                 'notifications': notifications,
#                 'unread_notifications_count': unread_count,
#             }
#         else:
#             print("User is not a hospital user.")
#     else:
#         print("User not authenticated.")
#     return {}

