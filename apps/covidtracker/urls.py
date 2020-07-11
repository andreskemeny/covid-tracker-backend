from django.urls import path, include
from .views import StatViewSet
from rest_framework import routers
router = routers.DefaultRouter()


# registramos nuestro api view al router
router.register("covid-stats", StatViewSet,
                basename="retrieve-summarized-stats")

# agregamos los urls del router a los urlpatterns
urlpatterns = [
    path("", include(router.urls))
]
