import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import serializers as serializers_core
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
from django.db.models import Count
from rest_framework.validators import ValidationError
from django.http import JsonResponse
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from user.models import Company, CompanyBranchDetail
from rest_framework import generics

from . import models
from . import serializers
from . import permissions as product_permission
from . import paginations
from . import filters
from user import models as user_models
from user import utils
from user import permissions as user_permission


class ProductOptionsAPIView(APIView):
    """ To send the product option info like (delivery time, metal, category, etc) """

    def get(self, request):
        product_options = {}
        data = {
            "data": {
                "delivery_time": [(obj.id, obj.time) for obj in models.DeliveryTime.objects.all()],
                "payment_type": [(obj.id, obj.type) for obj in models.PaymentType.objects.all()],
                "product_options": product_options,
                "product_options_id": {
                    "metal": [(obj.id, obj.name) for obj in models.Metal.objects.all()],
                    "metal_category": [(obj.id, obj.name) for obj in models.MetalCategory.objects.all()],
                    "metal_purity": [(obj.id, obj.name) for obj in models.MetalPurity.objects.all()]
                }
            }
        }
        print(data)
        for i in models.Commodity.objects.all():
            if product_options.get(i.matal.name) == None:
                product_options[i.matal.name] = {i.metal_category.name: [
                    purity.name for purity in i.metal_purity.all()]}
            else:
                product_options[i.matal.name][i.metal_category.name] = [purity.name for purity in i.metal_purity.all()]
        return Response(data=data, status=status.HTTP_201_CREATED)


# ======================================= Product Listing ==============================================

class ProductListView(ListAPIView):
    permission = [AllowAny]
    # TODO : set permission class
    queryset = models.Product.objects.filter(is_active=True, is_deleted=False)
    serializer_class = serializers.ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductFilters
    filterset_fields = ['trade', 'metal', 'metal_category', 'metal_purity', 'delivery_time', 'payment_type']
    pagination_class = paginations.ProductLimitOffsetPagination

# ======================================= Product List Preview ==============================================


class ProductListPreviewView(APIView):
    #     # permission_classes = [IsAuthenticated]
    #     # TODO : "Check the permission class"

    def get(self, request, *args, **kwargs):
        queryset = models.Product.objects.get(pk=kwargs['id'], is_active=True, is_deleted=False)
        serializer = serializers.ProductListPreviewSerializer(queryset)
        company = Company.objects.get(user_id=serializer.data['user'])
        company_branch_details_queryset = CompanyBranchDetail.objects.get(company=company)
        company_details_serilizer = serializers.CompanyDetailsForListPreviewSerializer(company_branch_details_queryset)
        return Response(
            data={'list_data': serializer.data, 'company_data': company_details_serilizer.data},
            status=status.HTTP_201_CREATED
        )

# ======================================= User Product Listing ==============================================


class UserProductListView(ListAPIView):

    # TODO : "Check the permission class"
    permission_classes = [AllowAny]
    serializer_class = serializers.UserProductListSerializer
    pagination_class = paginations.ProductLimitOffsetPagination

    def get_filter_attribute(self, filtering):
        profile_filters = {
            'active': [('is_active', True), ('is_deleted', False)],
            'stopped': [('is_active', False), ('is_deleted', True)],
            'paused': [('is_active', False), ('is_deleted', False)],
        }
        return profile_filters[filtering.lower()]

    def get_queryset(self):
        queryset = models.Product.objects.filter(user=self.request.user)
        get_parammeter = self.request.query_params
        if get_parammeter:
            condition = dict(self.get_filter_attribute(get_parammeter.get('status')))
            print(condition)
            queryset = queryset.filter(**condition)
        return queryset


# ======================================= User Product List Preview ==============================================


class UserProductListPreviewView(APIView):
    permission_classes = [AllowAny]
    # TODO : "Check the permission class"

    def get_filter_attribute(self, filtering):
        mylist_operation = {
            'active':  [('is_active', True), ('is_deleted', False)],
            'stop': [('is_active', False), ('is_deleted', True)],
            'pause': [('is_active', False), ('is_deleted', False)],
        }
        return mylist_operation[filtering.lower()]

    def get(self, request, *args, **kwargs):
        queryset = models.Product.objects.get(pk=kwargs['id'])
        serializer = serializers.UserProductListPreviewSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        get_parammeter = self.request.query_params
        if get_parammeter:
            condition = dict(self.get_filter_attribute(get_parammeter.get('status')))
            models.Product.objects.filter(pk=kwargs['id']).update(**condition)
            return Response({'message':  'Updation of the Operation Successful.'}, status=status.HTTP_201_CREATED)
        return Response({'message':  'Updation of the Operation not Successful.'}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Store Profile and Listing of that Product Owner  ==============================================


class StoreProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        get_parameter = self.request.query_params
        if get_parameter:
            store_id = get_parameter.get('store')
            bullion_details = models.Product.objects.get(pk=store_id, is_active=True, is_deleted=False)
            company_queryset = Company.objects.get(user_id=bullion_details.user)
            company_branch_queryset = CompanyBranchDetail.objects.get(company=company_queryset)
            company_brnach_serializer = serializers.StoreProfileSerializer(company_branch_queryset)

            # check store is_favourite
            current_user = user_models.User.objects.get(mobile_no=self.request.user.mobile_no)
            current_user_fav = current_user.favourites.all().values()
            fav_user_mobile_nos = [user_details['mobile_no'] for user_details in current_user_fav]
            is_favourite = True if bullion_details.user.mobile_no in fav_user_mobile_nos else False

            # List the Store Product
            list_query = models.Product.objects.filter(user=bullion_details.user, is_active=True, is_deleted=False)
            list_serializer = serializers.ProductListSerializer(list_query, many=True)

            print(type(company_brnach_serializer.data))

            return Response(
                {'store_details': {'details': company_brnach_serializer.data, "is_favourite": is_favourite},
                 'list_details': list_serializer.data},
                status=status.HTTP_201_CREATED)
        return Response(company_brnach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Favourites Section  ==============================================


class AddRemoveFavouritesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        get_parameter = self.request.query_params
        if get_parameter:
            company_branch_id = get_parameter.get('c_branch')
            company_branch_queryset = CompanyBranchDetail.objects.get(pk=company_branch_id)
            company_queryset = Company.objects.get(company_name=company_branch_queryset.company)
            user = user_models.User.objects.get(name=company_queryset.user_id)
            current_user = user_models.User.objects.get(mobile_no=request.user.mobile_no)

            if get_parameter.get('status').lower() == 'remove':
                current_user.favourites.remove(user)
                return Response({'message': 'Removed Successfully favourites'}, status=status.HTTP_201_CREATED)

            elif get_parameter.get('status').lower() == 'add':
                current_user.favourites.add(user)
                return Response({'message': 'Added Successfully favourites'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Nothing Performed'}, status=status.HTTP_400_BAD_REQUEST)


class UserMyFavouritesListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StoreProfileSerializer
    pagination_class = paginations.ProductLimitOffsetPagination

    def get_queryset(self):
        favourite_stores = list()
        current_user = user_models.User.objects.get(mobile_no=self.request.user.mobile_no)
        favourites = current_user.favourites.all()
        for favourite in favourites:
            company_queryset = Company.objects.get(user_id=favourite)
            company_branch_queryset = CompanyBranchDetail.objects.get(company=company_queryset)
            company_brnach_serializer = serializers.StoreProfileSerializer(company_branch_queryset)
            favourite_stores.append(company_brnach_serializer.data)
        return favourite_stores


class MyFavouritesUserProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        get_parameter = self.request.query_params
        if get_parameter:
            branch_id = get_parameter.get('c_branch')
            print(branch_id)
            company_branch_queryset = CompanyBranchDetail.objects.get(pk=branch_id)
            list_query = models.Product.objects.filter(user=company_branch_queryset.company.user_id)
            list_serializer = serializers.StoreProductListSerializer(list_query, many=True)
            return Response(list_serializer.data, status=status.HTTP_201_CREATED)
        return Response(list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Bid Rate Section  ==============================================

class BidRateListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = models.BidRate.objects.filter(bid_user=request.user)
        serializer = serializers.BidRateListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        get_parameter = self.request.query_params
        if get_parameter:
            product_id = get_parameter.get('p_id')
            product_query = models.Product.objects.get(pk=product_id)
            serializer = serializers.BidRateListSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if not models.BidRate.objects.filter(bid_user=self.request.user, bid_product=product_query):
                    serializer.save(bid_user=request.user, bid_product=product_query)
                    return Response({'message': "Sucessfully Bid Rate  Created"}, status=status.HTTP_201_CREATED)
                return Response({'message': "Same Bid Rate cannot create"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Unsucessfully Bid Rate "}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        get_parameter = self.request.query_params
        if get_parameter:
            remove = get_parameter.get('r_status')
            if remove != 'all':
                bid_query = models.BidRate.objects.get(pk=remove)
                bid_query.delete()
                return Response({'message':  'Bid Rate Deleted Successful.'}, status=status.HTTP_201_CREATED)
            elif remove == 'all':
                bid_query = models.BidRate.objects.get(bid_user=self.request.user)
                bid_query.delete()
                return Response({'message':  'Bid Rate Deleted Successful.'}, status=status.HTTP_201_CREATED)
            return Response({'message': "Unsucessfully Deletion of Bid Rate "}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= State And City  ==============================================

class StateListView(APIView):

    permission_classes = []

    def get(self, request, *args, **kwargs):
        queryset = models.State.objects.all()
        serializer = serializers.StateListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddStateCityView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_state', 'product.add_city']
        if utils.check_permission(request=request, permissions=permissions):
            serializer = serializers.AddStateCitySerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                city1 = models.City.objects.get_or_create(city_name=serializer.validated_data['city'])
                state1 = models.State.objects.get_or_create(state_name=serializer.validated_data['state'])
                state1[0].city.add(city1[0])
                print(state1, city1)
                return Response({"message": "State Added"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Commodities For State View  ==============================================

class ComoditiesForStateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_commodityforstate']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params.get('state')

            if get_parameter:
                try:
                    commodity_state_list = models.CommodityForState.objects.filter(state_id=get_parameter)
                    data = []
                    for commodity_state in commodity_state_list:
                        data.append({
                            'id': commodity_state.pk,
                            'metal': commodity_state.metal.name,
                            'metal_category': commodity_state.metal_category.name,
                            'purity': [purity.name for purity in commodity_state.metal_purity.all()],
                            'is_active': commodity_state.is_active
                        })

                except Exception as e:
                    raise ValidationError(detail=e)

            else:
                state_id_list = models.CommodityForState.objects.values('state_id').distinct()
                state_queryset = models.State.objects.filter(id__in=state_id_list).order_by('state_name')
                data = []
                for state in state_queryset:
                    data.append(
                        {
                            "id": state.pk,
                            "state": state.state_name
                        }
                    )
            if not data:
                raise ValidationError(detail={'details': "Wrongly Queried."})
            return Response(data=data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):

        if not ((request.user.is_admin and request.user.is_verified) or request.user.is_superuser):
            raise ValidationError(detail={'detail': 'You are not Authorized to do any changes'})
        permissions = ['product.add_commodityforstate']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.CommoditiesForStateSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    serializer.save()
                    return Response(
                        {"message": "Commdities Realted to Stated Added Sucessfully"},
                        status=status.HTTP_201_CREATED)
                except Exception as e:
                    raise ValidationError(detail={'message': e})
            return Response(serializer.errors['Exception Value'], status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

        permissions = ['product.change_commodityforstate']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.CommodityForState.objects.get(pk=int(get_parameter.get('id')))
                    print(queryset)
                    serailizer = serializers.CommoditiesForStateSerializer(queryset, data=self.request.data)
                    if serailizer.is_valid(raise_exception=True):

                        serailizer.save()
                        return Response(
                            {'message': "Commodity for State Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    raise ValidationError(detail={'message': e})
            return Response(
                {"message": "Enter the id to update the Commodity for State"},
                status=status.HTTP_400_BAD_REQUEST)


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================           Product Control Views               ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# ======================================= Metal View  ==============================================

class MetalView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_metal']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.Metal.objects.all()
            print(queryset)
            serailizer = serializers.MetalSerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_metal']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.MetalSerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Metal Added Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_metal']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.Metal.objects.get(pk=int(get_parameter.get('id')))
                    serailizer = serializers.MetalSerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response({'message': "Metal Updated Sucessfully"}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Metal Categories View  ==============================================

class MetalCategoryView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_metalcategory']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.MetalCategory.objects.all()
            print(queryset)
            serailizer = serializers.MetalCategorySerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_metalcategory']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.MetalCategorySerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Metal Category Added Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_metalcategory']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.MetalCategory.objects.get(pk=int(get_parameter.get('id')))
                    print(queryset)
                    serailizer = serializers.MetalCategorySerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response(
                            {'message': "Metal Category Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Metal Purity View  ==============================================

class MetalPurityView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_metalpurity']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.MetalPurity.objects.all()
            print(queryset)
            serailizer = serializers.MetalPuritySerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_metalpurity']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.MetalPuritySerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Metal Purity Added Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_metalpurity']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.MetalPurity.objects.get(pk=int(get_parameter.get('id')))
                    serailizer = serializers.MetalPuritySerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response(
                            {'message': "Metal Purity Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Payment Type  View  ==============================================

class PaymentTypeView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_paymenttype']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.PaymentType.objects.all()
            print(queryset)
            serailizer = serializers.PaymentTypeSerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_paymenttype']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.PaymentTypeSerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Payment Type Added Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_paymenttype']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.PaymentType.objects.get(pk=int(get_parameter.get('id')))
                    serailizer = serializers.PaymentTypeSerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response(
                            {'message': "Payment Type Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Delivery Time  View  ==============================================

class DeliveryTimeView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_deliverytime']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.DeliveryTime.objects.all()
            print(queryset)
            serailizer = serializers.DeliveryTypeSerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_deliverytime']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.DeliveryTypeSerailizer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Delivery Time Added Successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_deliverytime']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.DeliveryTime.objects.get(pk=int(get_parameter.get('id')))
                    serailizer = serializers.DeliveryTypeSerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response(
                            {'message': "Delivery Time Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# ======================================= Metal View  ==============================================

class MarketTimeView(APIView):

    permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

    def get(self, request, *args, **kwargs):
        permissions = ['product.view_markettime']
        if utils.check_permission(request=self.request, permissions=permissions):
            queryset = models.MarketTime.objects.all()
            print(queryset)
            serailizer = serializers.MarketTimeSerailizer(queryset, many=True)
            return Response(serailizer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        permissions = ['product.add_markettime']
        if utils.check_permission(request=self.request, permissions=permissions):
            serializer = serializers.MarketTimeSerailizer(data=request.data)
            if len(models.MarketTime.objects.all()) < 1:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"message": "Market Time Added Successfully"}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Already Exsists'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        permissions = ['product.change_markettime']
        if utils.check_permission(request=self.request, permissions=permissions):
            get_parameter = self.request.query_params
            if get_parameter.get('id'):
                try:
                    queryset = models.MarketTime.objects.get(pk=int(get_parameter.get('id')))
                    serailizer = serializers.MarketTimeSerailizer(queryset, data=request.data)
                    if serailizer.is_valid(raise_exception=True):
                        serailizer.save()
                        return Response(
                            {'message': "Market Time Updated Sucessfully"},
                            status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"message": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Enter the id to update the metal"}, status=status.HTTP_400_BAD_REQUEST)


# class StateCommoditiesView(APIView):
#     permission_classes = [user_permission.IsSuperAdminOrAdmin, user_permission.IsVerified]

#     def get(self, request, *args, **kwargs):
#         permissions = ['product.view_commodityforstate']
#         if utils.check_permission(request=self.request, permissions=permissions):
#             data = serializers_core.serialize(
#                 'json',
#                 [models.CommodityForState.objects.all()],
#                 fields=['state_id__state_name']
#             )
#             print(data)


# ===================================================================================
# ===================================================================================
# ===================================================================================
# ==================                                               ==================
# ==================                                               ==================
# ==================                Dummy Views                    ==================
# ==================                                               ==================
# ==================                                               ==================
# ===================================================================================
# ===================================================================================
# ===================================================================================


# class DummyAddStateCityView(APIView):

#     def post(self, request):
#         serializer = serializers.DummyAddStateCity(data=request.data)
#         if serializer.is_valid():
#             city1 = models.City.objects.get_or_create(city_name=serializer.validated_data['name'])
#             state1 = models.State.objects.get_or_create(state_name=serializer.validated_data['state'])
#             state1[0].city.add(city1[0])
#             print(state1, city1)
#             return Response({"message": "State Added"})
