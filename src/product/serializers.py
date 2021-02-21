from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    Product,
    MetalCategory,
    MetalPurity,
    Metal,
    DeliveryTime,
    PaymentType,
    BidRate,
    State,
    City,
    CommodityForState,
    MarketTime
)

from user.models import User, CompanyBranchDetail
from user import models as user_models


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['user', 'quantity', 'premium_value', 'premium_type', 'trade',
                  'metal', 'metal_purity', 'delivery_time', 'payment_type', 'metal_category']

        read_only_fields = ['user']


# ======================================== Prdouct Listing ================================================


class ProductListSerializer(serializers.ModelSerializer):
    trade = serializers.StringRelatedField()
    payment_type = serializers.StringRelatedField()
    delivery_time = serializers.StringRelatedField()
    metal = serializers.StringRelatedField()
    metal_category = serializers.StringRelatedField()
    metal_purity = serializers.StringRelatedField()

    class Meta():
        model = Product
        fields = ['id', 'trade', 'metal', 'metal_category', 'metal_purity',
                  'payment_type', 'premium_value', 'premium_type', 'delivery_time']


# ======================================== Prdouct List Preview ================================================


class CompanyDetailsForListPreviewSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta():
        model = CompanyBranchDetail
        fields = ['company', 'branch_address_line_1', 'branch_address_line_2',
                  'branch_city', 'branch_pincode', 'branch_state', 'branch_country']


class ProductListPreviewSerializer(serializers.ModelSerializer):
    trade = serializers.StringRelatedField()
    payment_type = serializers.StringRelatedField()
    metal = serializers.StringRelatedField()
    metal_category = serializers.StringRelatedField()
    metal_purity = serializers.StringRelatedField()

    class Meta():
        model = Product
        exclude = ['is_active', 'is_deleted', 'premium_type']
        read_only = ['user']


# ======================================== User Product Listing ================================================

class UserProductListSerializer(serializers.ModelSerializer):
    trade = serializers.StringRelatedField()
    metal = serializers.StringRelatedField()
    metal_category = serializers.StringRelatedField()
    metal_purity = serializers.StringRelatedField()

    class Meta():
        model = Product
        fields = ['id', 'trade', 'metal', 'metal_category', 'metal_purity', 'premium_value', 'is_active', 'is_deleted']


# ======================================== User Product List Preview ================================================


class UserProductListPreviewSerializer(serializers.ModelSerializer):
    trade = serializers.StringRelatedField()
    payment_type = serializers.StringRelatedField()
    delivery_time = serializers.StringRelatedField()
    metal = serializers.StringRelatedField()
    metal_category = serializers.StringRelatedField()
    metal_purity = serializers.StringRelatedField()

    class Meta():
        model = Product
        exclude = ['premium_type', 'user']


# ======================================== Store Profile ================================================
class StoreProfileSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta():
        model = CompanyBranchDetail
        fields = [
            'id', 'company', 'branch_address_line_1', 'branch_address_line_2', 'mobile_no1', 'mobile_no2',
            'geo_latitude', 'geo_longitude', 'branch_city', 'branch_pincode', 'branch_state', 'branch_country',
            'delivery_time']


class StoreProductListSerializer(serializers.ModelSerializer):
    trade = serializers.StringRelatedField()
    payment_type = serializers.StringRelatedField()
    delivery_time = serializers.StringRelatedField()
    metal = serializers.StringRelatedField()
    metal_category = serializers.StringRelatedField()
    metal_purity = serializers.StringRelatedField()

    class Meta():
        model = Product
        fields = ['id', 'trade', 'metal', 'metal_category', 'metal_purity',
                  'payment_type', 'premium_value', 'delivery_time']


# ======================================== Bid Rate  ================================================

class BidRateListSerializer(serializers.ModelSerializer):
    bid_user = serializers.StringRelatedField()
    bid_product = serializers.StringRelatedField()

    class Meta():
        model = BidRate
        fields = '__all__'

# ======================================== State And City List  Serailizer ================================================


class CityForStateListSerilizer(serializers.RelatedField):
    class Meta():
        model = City

    def to_representation(self, value):
        return value.city_name


class StateListSerializer(serializers.ModelSerializer):
    city = CityForStateListSerilizer(read_only=True, many=True)

    class Meta():
        model = State
        fields = ['id', 'state_name', 'city']


# ======================================== Add State And City Serailizer ================================================

class AddStateCitySerailizer(serializers.ModelSerializer):
    city = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)

    class Meta():
        model = State
        fields = ['city', 'state']

# ======================================== Commodities For State Serailizer ================================================


class CommoditiesForStateSerializer(serializers.ModelSerializer):
    # metal_purity = serializers.PrimaryKeyRelatedField(write_only=True)

    class Meta():
        model = CommodityForState
        fields = '__all__'


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================           Product Control Serializers         ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================

# ======================================== Metal  Serailizer ================================================


class MetalSerailizer(serializers.ModelSerializer):
    class Meta():
        model = Metal
        fields = ['id', 'name']


# ======================================== Metal Category Serailizer ================================================


class MetalCategorySerailizer(serializers.ModelSerializer):
    class Meta():
        model = MetalCategory
        fields = '__all__'


# ======================================== Metal Purity Serailizer ================================================


class MetalPuritySerailizer(serializers.ModelSerializer):
    class Meta():
        model = MetalPurity
        fields = '__all__'


# ======================================== Payment Type Serailizer ================================================


class PaymentTypeSerailizer(serializers.ModelSerializer):
    class Meta():
        model = PaymentType
        fields = '__all__'


# ======================================== Delivery Time Serailizer ================================================


class DeliveryTypeSerailizer(serializers.ModelSerializer):
    class Meta():
        model = DeliveryTime
        fields = '__all__'

# ======================================== Markekt Time Serailizer ================================================


class MarketTimeSerailizer(serializers.ModelSerializer):
    class Meta():
        model = MarketTime
        fields = '__all__'


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================             Dummy Serializers                 ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# ============================ Dummy Serializer for add State and city ==================================
