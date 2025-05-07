from django.urls import path
from . import views
from .views import donor_profile, custom_password_change
from django.contrib.auth import views as auth_views


# app_name = 'myapp'  # Set app_name as 'myapp'

urlpatterns = [
    path("login/", views.login_page, name='login'),
    path("", views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),

    path('forget-password/', views.ForgetPassword, name='forget-password'),
    path('password-reset-sent/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:signed_token>/', views.ResetPassword, name='reset-password'),


    path('adminn/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-hospital/<int:hospital_id>/', views.approve_hospital, name='approve_hospital'),
    path('request-blood/', views.request_blood, name='request_blood'),
    # path('manage-requests/', views.manage_blood_requests, name='manage_blood_requests'),
    # path('update-request-status/<int:request_id>/', views.update_blood_request_status, name='update_blood_request_status'),
    path("pending-hospitals/", views.pending_hospitals, name="pending_hospitals"),
    path('add_user/', views.add_user, name='add_user'),

    path('userlist/', views.UserListView.as_view(), name='user_list'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),

    # path('user/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),

    path('save/<int:pk>/', views.save_user, name='save_user'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    #admin blood request
    path('admin/blood-requests/', views.admin_blood_requests, name='admin_blood_requests'),
    path('admin/blood-request/<int:request_id>/', views.view_blood_request, name='view_blood_request'),
    path('admin/blood-request/delete/<int:request_id>/', views.delete_blood_request, name='delete_blood_request'),
    # path('admin/donor-response/delete/<int:response_id>/', views.delete_donor_response, name='delete_donor_response'),
    path('select-donor/<int:response_id>/', views.select_donor, name='select_donor'),
    path("unselect-donor/<int:response_id>/", views.unselect_donor, name="unselect_donor"),
    path('save_blood_donation/<int:response_id>/', views.save_blood_donation, name='save_blood_donation'),


    # Donor
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),  
    path('donor/available-requests/', views.available_blood_requests, name='available_blood_requests'),  
    path('donor/response/<int:request_id>/', views.donor_response, name='donor_response'), 

    path('inventory/', views.blood_inventory, name='blood_inventory'),
    path('inventory/add/<int:inventory_id>/', views.add_blood_units, name='add_blood_units'),
    path('inventory/subtract/<int:inventory_id>/', views.subtract_blood_units, name='subtract_blood_units'),
    path('inventory/update/<int:inventory_id>/', views.update_blood_inventory, name='update_blood_inventory'),
    # path('inventory/delete/<int:inventory_id>/', views.delete_blood_inventory, name='delete_blood_inventory'),
    path('admin/blood-inventory/clear/<int:inventory_id>/', views.clear_blood_inventory, name='clear_blood_inventory'),



    path('donor/profile/', views.donor_profile, name='donor_profile'),
    path('donor/profile/detail/', views.donor_profile_detail, name='donor_profile_detail'),
    path('donor/profile/update/', views.update_donor_profile, name='donor_profile_update'),
    path('password_change/', views.custom_password_change, name='password_change'),

    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('admin/profile/update/', views.admin_profile_update, name='admin_profile_update'),
    path('admin/password/change/', views.admin_password_change, name='admin_password_change'),


    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/profile/', views.hospital_profile, name='hospital_profile'),
    path('hospital/profile/detail/', views.hospital_profile_detail, name='hospital_profile_detail'),
    path('hospital/profile/update/', views.hospital_profile_update, name='hospital_profile_update'),
    path('hospital/profile/change-password/', views.hospital_password_change, name='hospital_password_change'),

    path('hospital/request-blood/', views.hospital_request_blood, name='hospital_request_blood'),
    path('hospital/requests/', views.hospital_view_requests, name='hospital_view_requests'),
    path('delete_request/<int:request_id>/', views.hospital_delete_request, name='hospital_delete_request'), 

    path('admin/hospital-requests/', views.admin_manage_hospital_requests, name='admin_manage_hospital_requests'),
    path('admin/hospital-request/<int:request_id>/accept/', views.admin_accept_request, name='admin_accept_request'),
    path('admin/hospital-request/<int:request_id>/reject/', views.admin_reject_request, name='admin_reject_request'),
    path('admin/hospital-request/<int:request_id>/delivered/', views.admin_mark_delivered, name='admin_mark_delivered'),
    path('admin/hospital-request/<int:request_id>/failed/', views.admin_mark_failed, name='admin_mark_failed'),



    # donation history in admin pannel
    path('donors/', views.DonorListView.as_view(), name='donor_list'),
    path('donor/<int:donor_id>/history/', views.donor_history, name='donor_history'),


    path('delivered/hospitals/', views.HospitalDeliverySummaryView.as_view(), name='hospital_delivery_summary'),
    path('delivered/hospital/<str:hospital_email>/', views.HospitalDeliveryDetailView.as_view(), name='hospital_delivery_detail'),

 ]

from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]

