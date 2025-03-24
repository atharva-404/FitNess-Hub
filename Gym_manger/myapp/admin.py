from django.contrib import admin
from .models import GymUser, Subscription, TrainerMessage,WorkoutVideo

class GymUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'number', 'subscription', 'plan', 'is_active', 'is_admin')
    list_filter = ('subscription', 'plan', 'is_active')
    search_fields = ('email', 'name', 'number')
    actions = ['activate_users', 'deactivate_users']

    fieldsets = (
        ("User Info", {'fields': ('email', 'name', 'number', 'age', 'weight', 'height', 'gender')}),
        ("Subscription Details", {'fields': ('subscription', 'plan')}),
        ("Permissions", {'fields': ('is_active', 'is_admin')}),
    )

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

admin.site.register(GymUser, GymUserAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'plan', 'amount', 'payment_status', 'created_at')
    list_filter = ('plan', 'payment_status')
    search_fields = ('name', 'email', 'phone')

admin.site.register(Subscription, SubscriptionAdmin)


class WorkoutVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'category')

admin.site.register(WorkoutVideo, WorkoutVideoAdmin)


class TrainerMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'trainer', 'timestamp')
    list_filter = ('trainer', 'timestamp')
    search_fields = ('user__name', 'trainer__name', 'message')

admin.site.register(TrainerMessage, TrainerMessageAdmin)
