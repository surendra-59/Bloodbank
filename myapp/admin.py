

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


# class UserModel(UserAdmin):
#     ordering = ('email',)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "user_type", "gender", "is_approved","blood_group","is_superuser",)
    search_fields = ("email","blood_group")
    # ordering = ("user_type[Hospital,User]","is_approved")
    ordering = ['-is_superuser', '-is_staff', 'user_type','date_joined']
    list_filter = ("is_approved", "user_type")

    #     -is_superuser: The minus sign - sorts in descending order (True first).
    # -is_staff: Similarly, this sorts is_staff in descending order.
    # user_type: Sorting by user_type in ascending order (with Hospital before User if it's represented numerically).

    # Remove 'username' and explicitly define fields
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    #     ("Personal Info", {"fields": ("organization_name","blood_group","contact_number","gender", "profile_pic","identity", "address")}),
    #     ("Important Dates", {"fields": ("last_login", "date_joined")}),
    #     ("Other Info", {"fields": ("user_type", "fcm_token","is_approved")}),
    #     ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        
    # )
    def get_fieldsets(self, request, obj=None):
        # Define the common fields for all users
        common_fieldsets = [
            ('User Info', {'fields': ['email', 'user_type','blood_group', 'dob', 'identity', 'gender', 'address', 'contact_number']}),
            ('Date Joined', {'fields': ['last_login', 'date_joined']}),
            ('Password', {'fields': ['password']}),
            ('Role', {'fields': ['is_approved', 'is_superuser', 'is_staff']}),
        ]
        
        if obj and obj.user_type == '2':  # If the user is a hospital (user_type == 2)
            # Fieldsets for hospital users (excluding first name, last name, dob, and blood group)
            return [
                ('Staff Info', {'fields': ['organization_name', 'identity']}),  # Staff Info comes first for hospitals
            ] + common_fieldsets  # Add the common fieldsets after Staff Info
        
        elif obj and obj.user_type == '3':  # If the user is a regular user (user_type == 3)
            # Fieldsets for regular users (excluding organization_name and identity)
            return [
                ('Personal Info', {'fields': ['first_name', 'last_name','profile_pic']}),
            ] + common_fieldsets  # Add the common fieldsets after Personal Info
        
        return common_fieldsets







# add_fieldsets is used in Django's 
#  custom admin panel to define the fields displayed 
#  when adding a new user (i.e., during user creation).


    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email","profile_pic","address", "password1", "password2", "user_type", "gender"
                ,"blood_group","identity","dob","contact_number"),
        }),
    )
    actions = ["approve_selected_staff"]

    def approve_selected_staff(self, request, queryset):
        queryset.update(is_approved=True)
        messages.success(request, "Selected staff members have been approved successfully.")


#Yes, approve_selected_staff is a function.
 # It is a custom admin action that you define to perform a specific operation on selected 
 # objects in the Django admin panel. The short_description is a string that provides a 
 # human-readable label for this action, which appears in the Django admin's action dropdown.

    
    approve_selected_staff.short_description = "Approve selected staff"

    # Add an approval button inside Django Admin panel
    def approve_action(self, obj):
        if not obj.is_approved:
            return format_html('<a class="button" href="/admin/approve-staff/{}/">Approve</a>', obj.id)
        return "Approved"

    approve_action.short_description = "Approval"

admin.site.register(CustomUser, CustomUserAdmin)





# admin.site.register(CustomUser, UserModel)

# In Django, actions is a built-in attribute of the ModelAdmin class,
#  not a method. It is used to specify custom actions that can be applied to 
#  selected items in the Django admin interface.

# How actions Works:
# actions is a list that holds the names of the functions that will be available as
#  actions in the admin panel.
# These actions will appear as options in the action dropdown at the top of the list of
#  items in the admin panel.
# Each action is a function that is defined to perform a specific operation on the selected objects.


# approve_action is called automatically by Django when rendering the list of users in the admin interface.
#  It is not something you explicitly call; rather, it is called for each user object when Django generates 
#  the HTML for the list.
# The button or status (Approved/Approve) is generated and displayed in the admin list view based on the
#  result of the approve_action method.