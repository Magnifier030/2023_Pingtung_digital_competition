from django.db import models

# Create your models here.
class Card(models.Model):
    card_id = models.CharField(max_length = 255, blank = True, primary_key = True)
    user_name = models.CharField(max_length = 255, blank = True)
    message = models.CharField(max_length = 255, blank = True)

    def __str__(self):
        return f"{self.card_id} {self.user_name} {self.message}"