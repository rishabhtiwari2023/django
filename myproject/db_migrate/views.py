# db_migrate/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item  # Ensure you are importing Item from models.py
from .tasks import create_item
import asyncio
import aiomysql

async def async_view(request):
	await asyncio.sleep(1)  # Simulate an async operation
	items = await Item.objects.all().values('name', 'description')
	return JsonResponse(list(items), safe=False)

def create_item_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        result = create_item.delay(name, description)
        return JsonResponse({'task_id': result.id, 'status': 'Task has been started'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#  curl -X POST -d "name=Sample Item&description=This is a sample description." http://localhost:8000/db_migrate/create-item/
# {"status": "Item creation task queued"}

async def async_db_query(request):
	conn = await aiomysql.connect(host='127.0.0.1', port=3306,
								  user='youruser', password='yourpassword',
								  db='yourdb')
	async with conn.cursor() as cur:
		await cur.execute("SELECT * FROM db_migrate_item")
		result = await cur.fetchall()
	conn.close()
	return JsonResponse(result, safe=False)

def create_item_view(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		description = request.POST.get('description')
		create_item.delay(name, description)  # Queue the task
		return JsonResponse({'status': 'Item creation task queued'})
	return JsonResponse({'status': 'Invalid request'}, status=400)