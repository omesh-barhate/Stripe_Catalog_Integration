from confluent_kafka import Producer
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

def add_to_queue(topic, data):
    producer.produce(topic, key=None, value=data)
    producer.flush()


def new_customer_event(action, customer):
    return {
        'action': action,
        'customer_id': customer.id,
        'customer_name': customer.name,
        'customer_email': customer.email
    }