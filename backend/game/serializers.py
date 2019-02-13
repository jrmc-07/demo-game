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
        fields = ('id', 'name', 'created',)


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
        if value.lower() not in {'box', 'color', 'move'}:
            raise serializers.ValidationError("action must be 'box', 'color', or 'move'.")
        return value


    def update(self, instance, validated_data):
        action = validated_data.pop('action').lower()
        if action == 'box':
            validated_data.pop('color', None)
            instance.validate_for_level('BX')
            validated_data['level'] = 'BX'
        elif action == 'color':
            pass
        elif action == 'move':
            validated_data.pop('color', None)
        # TODO elif action: unbox, uncolor

        return super().update(instance, validated_data)
