from django.contrib import admin

from webhooks.models import Webhook


# Register your models here.
@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_type",
        "event",
        "created_at",
        "updated_at",
    )
    list_filter = ("event_type",)
