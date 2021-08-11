from rest_framework.routers import DefaultRouter

#
from . import viewsets

router = DefaultRouter()

router.register(r'events', viewsets.EventViewSet, basename='events')
router.register(r'api/events', viewsets.CRUD_EventViewSet,
                basename='api-events')
# router.register(r'api/events/detail', viewsets.CRUD_DetailEventViewSet,
#                basename='api-events-detail')
router.register(r'events-by-user', viewsets.EventUser_ViewSet,
                basename='events-by-user')

urlpatterns = router.urls
