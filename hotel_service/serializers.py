from rest_framework import serializers
from .models import Room, Booking
from datetime import date

class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price"]


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]


class BookingCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ["id", "room_id", "date_start", "date_end"]

    def validate(self, attrs):
        ds = attrs.get("date_start")
        de = attrs.get("date_end")
        if ds >= de:
            raise serializers.ValidationError({"detail": "date_end должен быть позже date_start"})
        return attrs

    def create(self, validated_data):
        room_id = validated_data.pop("room_id")
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise serializers.ValidationError({"detail": "room_id не существует"})
        return Booking.objects.create(room=room, **validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Booking
        fields = ["booking_id", "date_start", "date_end"]
