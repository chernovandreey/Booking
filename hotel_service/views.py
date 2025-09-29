from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.utils.dateparse import parse_date

from .models import Room, Booking
from .serializers import (
    RoomCreateSerializer, RoomListSerializer,
    BookingCreateSerializer, BookingListSerializer
)


class RoomCreateView(APIView):
    def post(self, request):
        ser = RoomCreateSerializer(data=request.data)
        if ser.is_valid():
            room = ser.save()
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
        return Response({"detail": ser.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomDeleteView(APIView):
    def post(self, request):
        room_id = request.data.get("room_id") or request.query_params.get("room_id")
        if not room_id:
            return Response({"detail": "room_id обязателен."}, status=400)
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"detail": "Номер не найден."}, status=404)
        room.delete()  # каскадом удалит bookings
        return Response({"status": "ok"})


class RoomListView(APIView):
    def get(self, request):
        sort_by = request.query_params.get("sort_by", "created_at")
        order = request.query_params.get("order", "asc")

        allowed = {"price": "price", "created_at": "created_at"}
        field = allowed.get(sort_by, "created_at")
        ordering = field if order == "asc" else f"-{field}"

        qs = Room.objects.all().order_by(ordering, "id")
        data = RoomListSerializer(qs, many=True).data
        return Response(data)


class BookingCreateView(APIView):
    def post(self, request):
        # Принимаем: room_id, date_start, date_end (YYYY-MM-DD)
        ser = BookingCreateSerializer(data=request.data)
        if ser.is_valid():
            booking = ser.save()
            return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)
        # ser.errors уже в удобном JSON
        return Response({"detail": ser.errors.get("detail", ser.errors)}, status=400)


class BookingDeleteView(APIView):
    def post(self, request):
        booking_id = request.data.get("booking_id") or request.query_params.get("booking_id")
        if not booking_id:
            return Response({"detail": "booking_id обязателен."}, status=400)
        try:
            b = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"detail": "Бронь не найдена."}, status=404)
        b.delete()
        return Response({"status": "ok"})


class BookingListView(APIView):
    def get(self, request):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response({"detail": "room_id обязателен."}, status=400)
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({"detail": "Номер не найден."}, status=404)

        bookings = room.bookings.all().order_by("date_start", "id")
        data = BookingListSerializer(bookings, many=True).data
        return Response(data)
