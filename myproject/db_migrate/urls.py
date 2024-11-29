# db_migrate/urls.py
from django.urls import path
from .views import create_item_view, async_view, async_db_query

urlpatterns = [
	path('async-items/', async_view, name='async_items'),
	path('create-item/', create_item_view, name='create_item'),
	path('async-db-query/', async_db_query, name='async_db_query'),
]