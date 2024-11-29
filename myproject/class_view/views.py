from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from rest_framework import viewsets, generics, permissions, pagination, filters, throttling
from .models import Category
from .serializers import CategorySerializer

class ItemListCreateAPIView(APIView):
	def get(self, request):
		items = Item.objects.all()
		serializer = ItemSerializer(items, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = ItemSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemRetrieveUpdateDestroyAPIView(APIView):
	def get(self, request, pk):
		try:
			item = Item.objects.get(pk=pk)
		except Item.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = ItemSerializer(item)
		return Response(serializer.data)
	
	def put(self, request, pk):
		try:
			item = Item.objects.get(pk=pk)
		except Item.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = ItemSerializer(item, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		try:
			item = Item.objects.get(pk=pk)
		except Item.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = pagination.PageNumberPagination
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name', 'description']
	ordering_fields = ['name', 'id']
	throttle_classes = [throttling.UserRateThrottle]

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [permissions.IsAuthenticated]

class CustomItemView(generics.ListCreateAPIView):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer

	def get(self, request, *args, **kwargs):
		items = self.get_queryset()
		serializer = self.get_serializer(items, many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data)

# Versioning
class ItemViewSetV2(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = pagination.PageNumberPagination
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['name', 'description']
	ordering_fields = ['name', 'id']
	throttle_classes = [throttling.UserRateThrottle]

	def list(self, request, *args, **kwargs):
		response = super().list(request, *args, **kwargs)
		response.data['version'] = 'v2'
		return response
	# This viewset handles API operations for Item models, requires the user to be logged in, 
	# adds pagination, allows searching and sorting,
	# 	and limits the request rate. It also adds a version number (v2) to the list of items.