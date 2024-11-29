from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.broker_connection_retry_on_startup = True
# redis https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/
# sudo apt-get install lsb-release curl gpg
# curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
# sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
# echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
# sudo apt-get update
# sudo apt-get install redis

# sudo systemctl enable redis-server
# sudo systemctl start redis-server





# above code are worked

# sudo yum install redis
# sudo systemctl enable redis
# sudo systemctl start redis
# # sudo systemctl disable redis-server
# # sudo systemctl stop redis-server