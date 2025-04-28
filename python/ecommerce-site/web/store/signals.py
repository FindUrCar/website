from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import generate_product_description_task
from store.models import Product

@receiver(post_save, sender=Product)
def generate_description(sender, instance, created, **kwargs):
    if created and not instance.description:
        generate_product_description_task.delay(instance.id)
