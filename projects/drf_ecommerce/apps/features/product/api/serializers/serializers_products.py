# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.product.models import Products
from apps.features.product.api.serializers.serializers_measure_units import MeasureUnitsViewSerializer
from apps.features.product.api.serializers.serializers_categories_product import CategoriesProductViewSerializer

class ProductsViewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Products
        fields = '__all__'
    
    measure_unit = MeasureUnitsViewSerializer()
    category = CategoriesProductViewSerializer()
    stock = serializers.ReadOnlyField()  # <- Aquí accede a la propiedad @property del modelo
    
    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'name': instance.name,
    #         'description': instance.description,
    #         'measure_unit': {
    #             'id': instance.measure_unit.id,
    #             'description': instance.measure_unit.description
    #         } if instance.measure_unit else "",
    #         'category': {
    #             'id': instance.category.id,
    #             'description': instance.category.description
    #         } if instance.category else "",
    #         'image': instance.image.url if instance.image != "" else ""
    #     }

class ProductsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        exclude = ('id','is_active','created_at','updated_at','deleted_at')
    # measure_unit -> cuando se envie en el request debe ser obligatorio.
    def validate_measure_unit(self, measure_unit):
        if measure_unit in ['', None]:
            raise serializers.ValidationError('Debe ingresar un measure unit.')
        return measure_unit
    # category -> cuando se envie en el request debe ser obligatorio.
    def validate_category(self, category):
        if category in ['', None]:
            raise serializers.ValidationError('Debe ingresar un category.')
        return category
    
    def validate(self, instance):
        # measure_unit -> para obligar a que me envie el param en el request aunque en el model permita null.
        if 'measure_unit' not in instance.keys():
            raise serializers.ValidationError({
                'measure_unit': 'Debe ingresar un measure unit.'
            })
        # category -> para obligar a que me lo envie el param en el request aunque en el model permita null.
        if 'category' not in instance.keys():
            raise serializers.ValidationError({
                'category': 'Debe ingresar un category.'
            })
        return instance