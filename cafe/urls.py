from django.urls import path

from .views import meal_card, add_meal, list_meal, update_meal

app_name = "Cafe"
urlpatterns = [
    path("", list_meal, name="home"),
    path("service/<int:meal_id>", meal_card, name="service"),
    path("meal/add", add_meal, name="add_meal"),
    path("meal/<int:meal_id>/update", update_meal, name="update_meal"),
]
