from celery import Celery
from celery import shared_task
# from .models import Item
from django.conf import settings
from django.apps import apps
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('tasks', broker='redis://localhost:6379/')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@shared_task
def create_item(name, description):
    Item = apps.get_model('db_migrate', 'Item')
    Item.objects.create(name=name, description=description)

@app.task
def add(x, y):
    return x + y

@app.task
def print_message(message):
    print(message)
# result = print_message.delay('Hello, this is a test message!')
# print(f"Task result: {result.id}")
# r=add.delay(1, 7)
# print(r.id)
# result = create_item.delay('Sample Item', 'This is a sample description.')
# print(f"---------------------------------------Task result: {result.id}")




# celery -A db_migrate.tasks worker --loglevel=info