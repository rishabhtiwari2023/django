from django.shortcuts import render
from django.http import JsonResponse
from .models import SampleData
import json

# View to create sample data
def create_sample_data(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			name = data.get('name')
			value = data.get('value')
			SampleData.objects.create(name=name, value=value)
			
			# Store data in session
			request.session['last_created_name'] = name
			request.session['last_created_value'] = value
			request.session.set_expiry(300)  # Session expires in 5 minutes
			
			return JsonResponse({"message": "Sample data created"}, status=201)
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)
	return JsonResponse({"error": "Invalid request method"}, status=405)

def list_sample_data(request):
	data = SampleData.objects.all().values('name', 'value')
	return JsonResponse(list(data), safe=False)

# View to clear session data
def clear_session(request):
	request.session.clear()
	return JsonResponse({"message": "Session cleared"}, status=200)

# View to check if session was modified
def check_session_modified(request):
	if request.session.modified:
		return JsonResponse({"message": "Session was modified"}, status=200)
	else:
		return JsonResponse({"message": "Session was not modified"}, status=200)

# View using select_related() to fetch related objects in a single query
def list_sample_data_with_select_related(request):
	data = SampleData.objects.select_related('related_field').all().values('name', 'value', 'related_field__related_field_name')
	return JsonResponse(list(data), safe=False)

# View using prefetch_related() to fetch related objects in separate queries
def list_sample_data_with_prefetch_related(request):
	data = SampleData.objects.prefetch_related('related_field').all().values('name', 'value', 'related_field__related_field_name')
	return JsonResponse(list(data), safe=False)

# View using only() to fetch only specific fields
def list_sample_data_with_only(request):
	data = SampleData.objects.only('name', 'value').all().values('name', 'value')
	return JsonResponse(list(data), safe=False)

# View using defer() to defer fetching specific fields
def list_sample_data_with_defer(request):
	data = SampleData.objects.defer('large_field').all().values('name', 'value')
	return JsonResponse(list(data), safe=False)

# View using distinct() to fetch distinct records
def list_sample_data_with_distinct(request):
	data = SampleData.objects.values('name').distinct()
	return JsonResponse(list(data), safe=False)
