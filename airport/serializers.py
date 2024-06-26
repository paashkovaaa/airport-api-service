from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from airport.models import (Country,
                            City,
                            Airport,
                            AirplaneType,
                            Airplane,
                            Route,
                            Flight,
                            Order,
                            Ticket,
                            Crew)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ("id",
                  "name",
                  "rows",
                  "seats_in_row",
                  "airplane_type",
                  "image",)


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "capacity",
            "image",
        )


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id",
                  "route",
                  "airplane",
                  "departure_time",
                  "arrival_time",
                  "duration",
                  )


class RouteDetailSerializer(RouteListSerializer):
    flights = FlightSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
            "flights",
        )


class FlightListSerializer(FlightSerializer):
    route_source = serializers.CharField(
        source="route.source.name",
        read_only=True)
    route_destination = serializers.ImageField(
        source="route.destination.name",
        read_only=True)
    airplane_name = serializers.CharField(
        source="airplane.name", read_only=True
    )
    airplane_capacity = serializers.IntegerField(
        source="airplane.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route_source",
            "route_destination",
            "airplane_name",
            "airplane_capacity",
            "crew",
            "duration",
            "tickets_available",
        )


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneListSerializer(many=False, read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    airplane_image = serializers.ImageField(
        source="airplane.image", read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
            "airplane_image",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
