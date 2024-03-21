from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.country}-{self.name}"

    class Meta:
        ordering = ["name"]


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="airports")
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        ordering = ["name"]


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplanes")

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.airplane_type})"

    class Meta:
        ordering = ["name"]


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure_routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrival_routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.distance} km)"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    @property
    def duration(self) -> float | int:
        time_difference = self.arrival_time - self.departure_time
        total_seconds = time_difference.total_seconds()
        hours = total_seconds / 3600

        return hours

    def __str__(self):
        return f"{self.route}, {self.departure_time} -> {self.arrival_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order {self.id}: {self.user.last_name} {self.user.first_name}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"Row: {self.row}, seat: {self.seat}, flight: {self.flight}, {self.order.id}"
