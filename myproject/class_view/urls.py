from django.urls import path
from .views import ItemListCreateAPIView, ItemRetrieveUpdateDestroyAPIView
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CategoryViewSet, CustomItemView, ItemViewSetV2

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
	path('api/v1/', include(router.urls)),
     path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
	path('api/v1/custom-items/', CustomItemView.as_view(), name='custom-item-list'),
	path('api/v2/items/', ItemViewSetV2.as_view({'get': 'list', 'post': 'create'}), name='item-list-v2'),
	path('api/items/', ItemListCreateAPIView.as_view(), name='api-item-list-create'),
	path('api/items/<int:pk>/', ItemRetrieveUpdateDestroyAPIView.as_view(), name='api-item-rud'),
]

# from django.contrib.auth.models import User
# User.objects.create_user('testuser', 'testuser@example.com', 'testpassword')
# User.objects.create_user('your_username', 'your_email@example.com', 'your_password')
# curl -X POST http://127.0.0.1:8000/api-token-auth/      -H "Content-Type: application/json"      -d '{"username": "your_username", "password": "your_password"}'
# http://127.0.0.1:8000/class_view/api/items/      -H "Authorization: Token 169086b67fb491d78dae94e5468dcaff5cfad1ad"
#  curl -X POST http://127.0.0.1:8000/class_view/api/items/     -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37"     -H "Content-Type: application/json"     -d '{"name": "NewItem", "description": "This is a new item", "category": 1}'
#  curl -X POST http://127.0.0.1:8000/class_view/api/items/     -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37"     -H "Content-Type: application/json"     -d '{"name": "NewItem", "description": "This is a new item", "category": 1}'
# {"id":8,"name":"NewItem","description":"This is a new item","category":1} first create some cetegory the think about use this command
# curl -X PUT http://127.0.0.1:8000/api/items/1/ \
#      -H "Content-Type: application/json" \
#      -d '{"name": "UpdatedItem", "description": "This is an updated item", "category": 1}'


# curl -X GET http://127.0.0.1:8000/class_view/api/v1/custom-items/ -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37"
# curl -X GET http://127.0.0.1:8000/class_view/api/v1/items/ -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37"
# curl -X GET http://127.0.0.1:8000/class_view/api/v2/items/  -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37"  -H "Content-Type: application/json"
# curl -X GET http://127.0.0.1:8000/class_view/api/v2/items/ -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37" -H "Content-Type: application/json"
# {"count":8,"next":"http://127.0.0.1:8000/class_view/api/v2/items/?page=2","previous":null,
# "results":[{"id":1,"name":"NewItem","description":"This is a new item","category":1},{"id":2,"name":"NewItem","description":"This is a new item","category":1},{"id":3,"name":"NewItem","description":"This is a new item","category":1},{"id":4,"name":"NewItem","description":"This is a new item","category":1},{"id":5,"name":"NewItem","description":"This is a new item","category":1}], "version":"v2"}
# curl -X GET http://127.0.0.1:8000/class_view/api/v2/items/?page=2 -H "Authorization: Token 72df93fd30ebd851cab4f5bce77dec236f5b5b37" -H "Content-Type: application/json"
# {"count":8,"next":null,"previous":"http://127.0.0.1:8000/class_view/api/v2/items/","results":[{"id":6,"name":"NewItem","description":"This is a new item","category":1},{"id":7,"name":"NewItem","description":"This is a new item","category":1},{"id":8,"name":"NewItem","description":"This is a new item","category":1}],"version":"v2"}
