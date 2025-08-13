from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in seconds")

    def __str__(self):
        return self.title

class WatchSession(models.Model):
    DEVICE_CHOICES = [
        ("mobile", "Mobile"),
        ("web", "Web"),
        ("tv", "TV"),
        ("tablet", "Tablet"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    session_duration = models.PositiveIntegerField(editable=False)
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES)
    ip_address = models.GenericIPAddressField()
    is_rewatch = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.session_duration = max(
            0, int((self.end_time - self.start_time).total_seconds())
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.video}"
