# py
# django
# drf
from rest_framework import status
# third
# own
from apps.features.auth_own.tests.test_setup import TestSetUp
from apps.features.expense.models import Suppliers

class SuppliersTestCase(TestSetUp):
    
    def build_supplier_JSON(self):
        return {
            'ruc': '01234567891',
            'business_name': 'supplier 1',
            'address': 'Av. Quinta.',
            'phone': '0123456789',
            'email': 'supplier1@yopmail.com'
        }
    
    def test_search_supplier_by_ruc_status_code_200(self):
        supplier = Suppliers.objects.create(**self.build_supplier_JSON())
        response = self.client.get(
            '/expense/private_suppliers/search_supplier_by_ruc/',
            {
                'ruc': supplier.ruc
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier']['ruc'], supplier.ruc)
        # para parar en este punto y validar si va todo bien.
        # import pdb; pdb.set_trace()
    
    def test_serach_supplier_by_ruc_status_code_404(self):
        supplier = Suppliers.objects.create(**self.build_supplier_JSON())
        response = self.client.get(
            '/expense/private_suppliers/search_supplier_by_ruc/',
            {
                'ruc': 'XD'
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(supplier.ruc, 'XD')
        self.assertEqual(response.data['message'], 'No se ha encontrado un supplier con el RUC proporcionado.')
        # para parar en este punto y validar si va todo bien.
        # import pdb; pdb.set_trace()
        
    def test_serach_supplier_by_ruc_status_code_400(self):
        supplier = Suppliers.objects.create(**self.build_supplier_JSON())
        response = self.client.get(
            '/expense/private_suppliers/search_supplier_by_ruc/',
            {},
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Debe proporcionar el RUC del supplier.')
        # para parar en este punto y validar si va todo bien.
        # import pdb; pdb.set_trace()
    
    def test_new_supplier_status_code_200(self):
        supplier = self.build_supplier_JSON()
        response = self.client.post(
            '/expense/private_suppliers/',
            supplier,
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['ruc'], supplier['ruc'])
        self.assertEqual(Suppliers.objects.all().count(), 1)
        # para parar en este punto y validar si va todo bien.
        # import pdb; pdb.set_trace()