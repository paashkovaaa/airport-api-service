from django.urls import path, include
from rest_framework import routers

from airport.views import CrewViewSet, CountryViewSet, CityViewSet, AirportViewSet, AirplaneTypeViewSet, \
    AirplaneViewSet, RouteViewSet, FlightViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("country", CountryViewSet)
router.register("city", CityViewSet)
router.register("airport", AirportViewSet)
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("route", RouteViewSet)
router.register("flight", FlightViewSet)
router.register("order", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
