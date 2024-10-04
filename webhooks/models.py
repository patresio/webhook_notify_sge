import uuid

from django.db import models


# Create your models here.
class Webhook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system = models.CharField(max_length=50, null=True, blank=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.system} - {str(self.id)} - {self.event_type}"
