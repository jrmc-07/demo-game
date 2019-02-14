import webcolors
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    position_counter = models.IntegerField(default=6)


class Player(models.Model):
    LEVEL_CHOICES = (
        ('RE', 'Regular'),
        ('BX', 'Boxed'),
        ('CO', 'Colored'),
    )
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    position = models.IntegerField()
    color = models.CharField(max_length=25, default="#ffffff")
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        default='RE',
    )

    class Meta:
        unique_together = ('game', 'position')

    def get_color_name(self):
        try:
            return webcolors.hex_to_name(self.color)
        except ValueError:
            # default to while on broken color
            return "white"

    def validate_for_level(self, level):
        """
        BX requires:
        - current level is RE
        CO requires:
        - current level is BX
        RE requires:
        - current level is BX
        """
        if level == 'BX':
            assert self.level == 'RE', "Player isn't registered. Can't be boxed."
        elif level == 'CO':
            assert self.level == 'BX', "Player isn't boxed. Can't be colored."
        elif level == 'RE':
            assert self.level == 'BX', "Player isn't boxed. Can't be unboxed."
        else:
            raise AssertionError("Invalid level")

