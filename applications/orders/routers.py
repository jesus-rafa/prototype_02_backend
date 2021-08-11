from rest_framework.routers import DefaultRouter
#
from . import viewsets


router = DefaultRouter()

router.register(r'orders', viewsets.OrdersViewSet, basename='orders')

urlpatterns = router.urls
