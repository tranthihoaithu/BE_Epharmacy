from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Epharmacy API",
        default_version='v1',
        description="APIs for Epharmacy",
        contact=openapi.Contact(email="tranhoaithu@gmail.com"),
        license=openapi.License(name="Trần Hoài Thu "),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

router = DefaultRouter()
router.register('medicine', views.PharmacyViewSet)
router.register('user', views.UserViewSet)


# medicine/ -GET
# /medicine/ -POST
# /medicine/{id_medicine} -GET
# /medicine/{id_medicine} -PUT
# /medicine/{id_medicine} -DELETE
urlpatterns = [
    path('', include(router.urls)),
    # path('admin/', admin.site.urls),
    path('order/<int:id>/', views.order, name='order'),
    path('medicine/', views.MedicineSerializer),
    path('admin/', admin_site.urls),
    path('thuoc/', views.get_all_medicines, name='thuoc'),
    path('thuoc/<id>/', views.get_detail_medicine, name='detail_medicine'),
    path('api/register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('api/login/', views.LoginUserAPIView.as_view(), name='login'),
    path('api/cart/add/', views.CartViewSet.as_view(), name='cart'),
    path('api/remove_from_cart/<int:item_id>/', views.CartViewSet.as_view(), name='remove_from_cart'),
    path('api/update_quantity/', views.CartViewSet.as_view(), name='update_quantity'),
    path('api/cart/item/<str:username>/', views.get_item_cart, name='item_cart'),
    path('api/order/<str:username>/', views.checkout, name='order'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
