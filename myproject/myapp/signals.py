import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('transaction_logs.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@receiver(post_save, sender=Transaction)
def log_transaction(sender, instance, created, **kwargs):
	if created:
		log_message = f"Transaction logged: {instance.transaction_type} of {instance.amount} from {instance.from_account} to {instance.to_account}"
		logger.info(log_message)