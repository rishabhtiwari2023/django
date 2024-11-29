from django.urls import path
from . import views

urlpatterns = [
	path('create/', views.create_sample_data, name='create_sample_data'),
	path('list/', views.list_sample_data, name='list_sample_data'),
	path('list/select_related/', views.list_sample_data_with_select_related, name='list_sample_data_with_select_related'),
	path('list/prefetch_related/', views.list_sample_data_with_prefetch_related, name='list_sample_data_with_prefetch_related'),
	path('list/only/', views.list_sample_data_with_only, name='list_sample_data_with_only'),
	path('list/defer/', views.list_sample_data_with_defer, name='list_sample_data_with_defer'),
	path('list/distinct/', views.list_sample_data_with_distinct, name='list_sample_data_with_distinct'),
	path('session/clear/', views.clear_session, name='clear_session'),
	path('session/check_modified/', views.check_session_modified, name='check_session_modified'),
]




# curl -X POST http://127.0.0.1:8000/sqlviewer/create/ -H "Content-Type: application/json" -d '{"name": "Sample1", "value": 100}'
# curl http://127.0.0.1:8000/sqlviewer/list/
# curl http://127.0.0.1:8000/sqlviewer/list/only/
# curl http://127.0.0.1:8000/sqlviewer/list/defer/
# curl http://127.0.0.1:8000/sqlviewer/list/distinct/
# curl http://127.0.0.1:8000/sqlviewer/session/clear/
# curl http://127.0.0.1:8000/sqlviewer/session/check_modified/