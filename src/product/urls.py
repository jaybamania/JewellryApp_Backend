from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewset import ProductCreateViewSet

from . import views

router = DefaultRouter()
router.register('', ProductCreateViewSet, basename='Product Create')


urlpatterns = [
    path('', include(router.urls)),
    path('options/', views.ProductOptionsAPIView.as_view()),
    path('list/', views. ProductListView.as_view(), name='Product List'),
    path('list/<int:id>/', views.ProductListPreviewView.as_view(), name='Product Preview List'),
    path('mylisting/', views.UserProductListView.as_view(), name='User Product'),
    path('mylisting/<int:id>/', views.UserProductListPreviewView.as_view(), name='User Product Preview'),
    path('storedetails/', views.StoreProfileView.as_view(), name='store details'),
    path('favouritesoper/', views.AddRemoveFavouritesView.as_view(), name='favourites operation'),
    path('myfavourites/', views.UserMyFavouritesListView.as_view(), name='Myfavourites'),
    path('myfavourites/list/', views.MyFavouritesUserProductListView.as_view(), name='Myfavourites List'),
    path('mybid/', views.BidRateListView.as_view(), name='Bid List'),

    path('state/list/', views.StateListView.as_view(), name="State List"),
    path('state/', views.AddStateCityView.as_view(), name="State and City Add"),
    path('commodity/', views.ComoditiesForStateView.as_view(), name="List of State for Commodities"),
    # path('commodity/<int:id>/', views.ComoditiesForStateView.as_view(), name="Commodity Relation with State"),
    path('metal/', views.MetalView.as_view(), name="Metal Operations"),
    path('metalcategory/', views.MetalCategoryView.as_view(), name="Metal Category Operations"),
    path('metalpurity/', views.MetalPurityView.as_view(), name="Metal Purity Operation"),
    path('paymenttype/', views.PaymentTypeView.as_view(), name='Payment Type Operation'),
    path('deliverytime/', views.DeliveryTimeView.as_view(), name='Delivery Time Operation'),
    path('markettime/', views.MarketTimeView.as_view(), name='Market Time Operation'),

]
