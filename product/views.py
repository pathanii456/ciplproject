from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from product.permissions import IsAdminOrReadOnly
from product.filters import ProductFilter
from product.renderers import ProductRenderer
from django.http import HttpResponse
import openpyxl
# from rest_framework.permissions import IsAdminUser
# from rest_framework.decorators import permission_classes
from rest_framework.views import APIView


# API to create a new product.
class ProductCreateView(generics.CreateAPIView):
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# API to update an existing product by ID (Admins only).
class ProductUpdateView(generics.UpdateAPIView):
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# API to delete (soft delete) a product by ID (Admins only).
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def destroy(self, request, *args, **kwargs):
        # Perform the soft delete
        instance = self.get_object()
        self.perform_destroy(instance)

        # Return a custom response
        return Response(
            {"message": "Product soft-deleted successfully"},
            status=status.HTTP_200_OK
        )


class ProductListView(generics.ListAPIView):
    """
    API to list all products (Admins and Users).
    Supports filtering, sorting, and pagination.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter]
    filterset_class = ProductFilter  # Use your custom filter class here
    ordering_fields = ['created_on', 'updated_on']
    search_fields = ['title', 'description']


class ProductDisableView(generics.UpdateAPIView):
    """
    API to disable a product by ID (Admins only).
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({"message": "Product disabled successfully"})
    

class ExportProductsView(APIView):
    renderer_classes = [ProductRenderer]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Products"
        # Add headers
        sheet.append(['ID', 'Title', 'Description', 'Price', 'Discount', 'Image', 'SSN', 'Is Active', 'Created On', 'Updated On'])
        
        # Add data
        for product in products:
            # Format the fields as needed
            image_url = product.image.url if product.image else 'No image'
            row = [
                product.id,
                product.title,
                product.description,
                f"${product.price:.2f}",  # Format price to 2 decimal places
                f"{product.discount:.2f}",  # Format discount to 2 decimal places
                image_url,  # Provide the image URL or 'No image'
                product.ssn,
                product.is_active,
                product.created_on.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
                product.updated_on.strftime("%Y-%m-%d %H:%M:%S"),  # Format datetime
            ]
            sheet.append(row)

        # Prepare the response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'

        workbook.save(response)
        return response
