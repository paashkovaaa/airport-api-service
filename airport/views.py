from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from airport.models import (Crew,
                            Country,
                            City,
                            Airport,
                            AirplaneType,
                            Airplane,
                            Route,
                            Order,
                            Flight)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (CountrySerializer,
                                 CrewSerializer,
                                 CitySerializer,
                                 AirportSerializer,
                                 AirplaneTypeSerializer,
                                 AirplaneSerializer,
                                 RouteSerializer,
                                 OrderSerializer,
                                 OrderListSerializer,
                                 FlightSerializer,
                                 AirplaneImageSerializer,
                                 FlightListSerializer,
                                 FlightDetailSerializer,
                                 AirplaneListSerializer,
                                 RouteListSerializer,
                                 RouteDetailSerializer)


class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CountryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = Pagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CityViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = Pagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = Pagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.prefetch_related("airplane_type")
    pagination_class = Pagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the airplanes with filters"""
        name = self.request.query_params.get("name")
        airplane_types = self.request.query_params.get("airplane_types")
        capacity_gte = self.request.query_params.get("capacity_gte")

        queryset = self.queryset.annotate(
            total_capacity=F("rows") * F("seats_in_row")
        )

        if name:
            queryset = queryset.filter(name__icontains=name)

        if airplane_types:
            airplane_type_ids = self._params_to_ints(airplane_types)
            queryset = queryset.filter(airplane_type__id__in=airplane_type_ids)

        if capacity_gte:
            queryset = queryset.filter(total_capacity__gte=capacity_gte)

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "airplane_types",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by airplane_type ids "
                            "(ex. ?airplane_types=1,2)",
            ),
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by airplane name (ex. ?name=Airplane)",
            ),
            OpenApiParameter(
                "capacity_gte",
                type=OpenApiTypes.NUMBER,
                description="Filter by capacity "
                            "greater than or equal to the "
                            "specified value (ex. ?capacity_gte=200)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.all().select_related("source", "destination")
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = (
        Flight.objects.all()
        .select_related("route__source",
                        "route__destination",
                        "airplane__airplane_type")
        .annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        airplanes = self.request.query_params.get("airplanes")
        routes = self.request.query_params.get("routes")
        date = self.request.query_params.get("date")

        queryset = self.queryset

        if airplanes:
            airplanes_ids = self._params_to_ints(airplanes)
            queryset = queryset.filter(airplane__id_in=airplanes_ids)

        if routes:
            routes_ids = self._params_to_ints(routes)
            queryset = queryset.filter(route__id__in=routes_ids)

        if date:
            queryset = queryset.filter(departure_time__date=date)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "airplanes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by airplane ids (ex. ?airplanes_ids=1,2)",
            ),
            OpenApiParameter(
                "routes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by routes ids (ex. ?routes=1,2)",
            ),
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description="Filter by flight date (ex. ?date=2025-06-22)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.select_related(
        "tickets__flight__route", "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
