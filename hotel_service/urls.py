from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter,"year4")


urlpatterns = [
    path('', views.index, name='home'),
    path('rooms/<int:room_id>', views.rooms, name='rooms_id'),
    path('rooms/<slug:room_slug>', views.rooms_by_slug, name='rooms'),
    path(r"archive/<year4:year>/", views.archive, name='archive'),

]