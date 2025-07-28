from django.db import models

# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=200)
    fallower_count = models.IntegerField(default=0)
    alert_threshold = models.IntegerField(default=1000)
    telegram_chat_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username