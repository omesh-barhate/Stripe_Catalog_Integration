from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .kafka import add_to_queue, new_customer_event
import json

class Customer(models.Model):
    id=models.CharField(primary_key=True,max_length=250)
    name=models.CharField(max_length=700)
    email=models.EmailField()
    
    def __str__(self):
        return self.id

@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, **kwargs):
    if kwargs.get('created', False):
        action = 'customer_created'
    else:
        action = 'customer_updated'
    event = new_customer_event(action, instance)
    add_to_queue('customer_events', json.dumps(event).encode('utf-8'))

@receiver(post_delete, sender=Customer)
def customer_deleted(sender, instance, **kwargs):
    action='customer_deleted'
    event = new_customer_event(action, instance)
    add_to_queue('customer_events', json.dumps(event).encode('utf-8'))