from django.urls import path, include
from .views import StatViewSet
from rest_framework import routers
router = routers.DefaultRouter()

router.register("covid-stats", StatViewSet,
                basename="retrieve-summarized-stats")

urlpatterns = [
    path("", include(router.urls))
]
