from django.contrib import admin

from webhooks.models import Webhook


# Register your models here.
@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "system",
        "event_type",
        "created_at",
        "updated_at",
    )
    list_filter = ("event_type",)
