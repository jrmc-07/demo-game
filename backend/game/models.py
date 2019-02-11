from django.db import models


class Player(models.Model):
    LEVEL_CHOICES = (
        ('RE', 'Regular'),
        ('BX', 'Boxed'),
        ('CO', 'Colored'),
    )
    name = models.CharField(max_length=25)
    position = models.IntegerField(unique=True)
    color = models.CharField(max_length=25)
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default='RE',
    )
