"""
URL configuration for sitehotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotel_service.views import (
    RoomCreateView, RoomDeleteView, RoomListView,
    BookingCreateView, BookingDeleteView, BookingListView
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rooms
    path("rooms/create", RoomCreateView.as_view()),
    path("rooms/delete", RoomDeleteView.as_view()),
    path("rooms/list",   RoomListView.as_view()),

    # Bookings
    path("bookings/create", BookingCreateView.as_view()),
    path("bookings/delete", BookingDeleteView.as_view()),
    path("bookings/list",   BookingListView.as_view()),
]
