# py
# django
# drf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
# thrid
from drf_yasg import openapi # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.expense.api.serializers.serializers import (
    SuppliersViewSerializer,
    SuppliersActionsSerializer
)

class PublicSuppliersViewSets(PublicGeneralViewSets):
    serializer_class = SuppliersActionsSerializer
    serializer_view_class = SuppliersViewSerializer
    
    def list(self, request, *args, **kwargs):
        suppliers = self.get_queryset()
        suppliers_serializer = self.get_serializer(suppliers, many = True)
        return Response(suppliers_serializer.data,status=status.HTTP_200_OK)

class PrivateSuppliersModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = SuppliersActionsSerializer
    serializer_view_class = SuppliersViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        supplier = self.get_object()
        if supplier:
            supplier.is_active = False
            supplier.save()
            return Response({'message':'Successfully Supplier elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Supplier elimination.'},status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'ruc',
                openapi.IN_QUERY,
                description="RUC del proveedor",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response('Proveedor encontrado.'),
            400: openapi.Response('Solicitud incorrecta.'),
            404: openapi.Response('Proveedor no encontrado.')
        },
        operation_summary="Buscar supplier por RUC",
        operation_description="Este endpoint permite buscar un supplier (proveedor) por su RUC."
    )
    @action(detail=False, methods=['get'])
    def search_supplier_by_ruc(self, request):
        ruc = request.query_params.get('ruc')
        if not ruc:
            return Response({
                'message': 'Debe proporcionar el RUC del supplier.'
            }, status=status.HTTP_400_BAD_REQUEST)

        supplier = self.get_serializer_class().Meta.model.objects.filter(ruc__iexact=ruc).first()

        if supplier:
            supplier_serializer = self.serializer_view_class(supplier)
            return Response({
                'supplier': supplier_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'No se ha encontrado un supplier con el RUC proporcionado.'
        }, status=status.HTTP_404_NOT_FOUND)