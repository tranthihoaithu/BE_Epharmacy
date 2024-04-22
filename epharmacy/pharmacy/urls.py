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


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('index/', views.index, name='index'),

    path('api/register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('api/login/', views.LoginUserAPIView.as_view(), name='login'),

    path('thuoc/', views.get_all_medicines, name='thuoc'),
    path('thuoc/<id>/', views.get_detail_medicine, name='detail_medicine'),

    path('api/category/', views.get_all_category, name='category'),
    path('api/category/<int:category_id>/', views.get_category_medicine, name='category_product'),

    path('api/cart/add/', views.CartViewSet.as_view(), name='cart'),
    path('api/remove_from_cart/<int:item_id>/', views.CartViewSet.as_view(), name='remove_from_cart'),
    path('api/update_quantity/<int:item_id>/', views.CartViewSet.as_view(), name='update_quantity'),
    path('api/cart/item/<str:username>/', views.get_item_cart, name='item_cart'),

    path('api/order/<str:username>/', views.checkout, name='order'),

    path('api/discount/<int:medicine_id>/', views.get_discount, name='discount'),



    path('api/user/', views.UserListAPIView.as_view(), name='user'),

    path('api/invoice/', views.generate_pdf, name='invoice'),


    path('api/history/<int:user_id>/', views.HistoryViewSet.as_view(), name='history'),
    path('api/history/detail_item/<int:order_id>/', views.HistoryViewSet.as_view(), name='history'),
    path('search/', views.SearchResultsView.as_view(), name='search'),

]
