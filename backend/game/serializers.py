import traceback
import webcolors
from rest_framework import serializers

from .models import Game, Player


class ColorField(serializers.CharField):
    """
    Takes a color name and stores it in hex form. Representation is the color name.
    """
    def to_representation(self, value):
        try:
            return webcolors.hex_to_name(value)
        except ValueError:
            return "white"

    def to_internal_value(self, data):
        try:
            # force an error as validation
            color_name = webcolors.name_to_hex(data)
        except ValueError:
            raise serializers.ValidationError("Invalid color name.")

        return super().to_internal_value(color_name)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'created', 'position_counter',)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id',)


class PlayerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name',)


class PlayerListSerializer(serializers.ModelSerializer):
    color = ColorField()

    class Meta:
        model = Player
        fields = ('id', 'name', 'position', 'color', 'level',)


class PlayerUpdateSerializer(serializers.ModelSerializer):
    color = ColorField(required=False)
    action = serializers.CharField(write_only=True)

    class Meta:
        model = Player
        fields = ('id', 'action', 'position', 'color', 'level',)
        read_only_fields = ('position', 'level',)

    def validate_action(self, value):
        if value.lower() not in {'box', 'color', 'move', 'kick', 'uncolor'}:
            raise serializers.ValidationError("action must be 'box', 'color', 'kick', 'uncolor' or 'move'.")
        return value


    def update(self, instance, validated_data):
        action = validated_data.pop('action').lower()
        try:
            if action == 'box':
                validated_data.pop('color', None)
                instance.validate_for_level('BX')
                validated_data['level'] = 'BX'

            elif action == 'color':
                instance.validate_for_level('CO')
                assert 'color' in validated_data, "Color must not be empty."
                validated_data['level'] = 'CO'

            elif action == 'move':
                validated_data.pop('color', None)
                assert instance.level == 'BX', "Player must be boxed to move."
                assert instance.position > 1, "Can't move any further!"
                # get game board
                game_board = {x for x in range(1, instance.position)}
                # remove not allowed spaces
                colored_positions = (
                    Player.objects
                    .filter(game=instance.game,
                            level="CO")
                    .values_list('position', flat=True)
                )
                for pos in colored_positions:
                    game_board.discard(pos)
                # starting from the bottom
                candidate_idx = max(game_board)
                while 1:
                    try:
                        candidate_player = Player.objects.get(
                            position=candidate_idx,
                            game=instance.game)
                    except Player.DoesNotExist:
                        # free space
                        validated_data['position'] = candidate_idx
                        break
                    if candidate_player.level == "RE":
                        # swap
                        candidate_player.position = instance.position
                        instance.position = -1
                        instance.save()
                        candidate_player.save()
                        validated_data['position'] = candidate_idx
                        break
                    elif candidate_player.level == "BX":
                        raise Exception("Kick before moving.")
                    # level is "CO"
                    game_board.discard(x)
                    candidate_idx = max(game_board)

            elif action == 'kick':
                validated_data.pop('color', None)
                assert instance.level == 'BX', "Player must be boxed to kick."
                # get game board
                game_board = {x for x in range(1, instance.position)}
                # remove not allowed spaces
                colored_positions = (
                    Player.objects
                    .filter(game=instance.game,
                            level="CO")
                    .values_list('position', flat=True)
                )
                for pos in colored_positions:
                    game_board.discard(pos)
                # starting from the bottom
                candidate_idx = max(game_board)
                try:
                    candidate_player = Player.objects.get(
                        position=candidate_idx,
                        game=instance.game)
                except Player.DoesNotExist:
                    # free space
                    raise Exception("Can't kick empty space!")
                assert candidate_player.level == "BX", "Can only kick boxed player!"
                candidate_player.level = "RE"
                candidate_player.save()

            elif action == 'uncolor':
                validated_data.pop('color', None)
                assert instance.level == 'CO', "Player must be colored to uncolor."
                validated_data['level'] = 'BX'

        except ValueError:
            raise serializers.ValidationError({"message": "Can't move any further!"})
        except Exception as e:
            raise serializers.ValidationError({"message": str(e)})

        return super().update(instance, validated_data)
