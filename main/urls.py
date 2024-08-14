from django.urls import path
from django.urls.conf import include

from .views import index, UserViewSet, CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, check_active_orders
from rest_framework import routers
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tezbiyor API",
        default_version='v1',
        description="...",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderitem', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', index, name='index'),
    path('orders/admin/', check_active_orders, name='check_active_orders'),
    path('', include(router.urls))
]
