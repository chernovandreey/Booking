# docker compose up --build
# web: http://localhost:9000
# postgres для DBeaver: 127.0.0.1:5433

# Запросы:
# создать номер
curl -X POST -d "description=Уютный номер" -d "price=3500.00" http://localhost:9000/rooms/create
# списки номеров
curl "http://localhost:9000/rooms/list?sort_by=price&order=asc"
curl "http://localhost:9000/rooms/list?sort_by=created_at&order=desc"
# создать бронь
curl -X POST -d "room_id=1" -d "date_start=2021-12-30" -d "date_end=2022-01-02" http://localhost:9000/bookings/create
# список броней номера
curl "http://localhost:9000/bookings/list?room_id=1"
# удалить бронь или номер
curl -X POST -d "booking_id=1" http://localhost:9000/bookings/delete
curl -X POST -d "room_id=1"     http://localhost:9000/rooms/delete
