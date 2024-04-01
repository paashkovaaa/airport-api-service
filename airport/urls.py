from django.urls import path, include
from rest_framework import routers

from airport.views import CrewViewSet, CountryViewSet, CityViewSet, AirportViewSet, AirplaneTypeViewSet, \
    AirplaneViewSet, RouteViewSet, FlightViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
