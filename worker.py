from confluent_kafka import Consumer, KafkaError
import stripe
import json

CUSTOMER_CREATED_EVENT = 'customer_created'
CUSTOMER_DELETED_EVENT = 'customer_deleted'
CUSTOMER_UPDATED_EVENT = 'customer_updated'

stripe.api_key = "sk_test_51O6uYYSA6FlGwjPeGp7oRWpHKOFb74z6U45KYislv8nXsWQntNGr6R8ujI3gkW3cKHSrSz5LtMpe3BdpePe4XRmN00pO2BxfNJ"

kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
kafka_consumer = Consumer(kafka_config)
kafka_consumer.subscribe(['customer_events'])

def check_event(msg):
    message = json.loads(msg.value())
    action = message.get('action')
    customer_id = message.get('customer_id')
    customer_name = message.get('customer_name')
    customer_email = message.get('customer_email')
    if action == CUSTOMER_CREATED_EVENT:
        try:
            stripe.Customer.create(
                name=customer_name,
                email=customer_email
            )
            print(f"Customer {customer_id} created on Stripe")
        except Exception as e:
            print(f"Error creating customer {customer_id} on Stripe: {e}")
    
    elif action == CUSTOMER_UPDATED_EVENT:
        try:
            stripe.Customer.modify(
                customer_id,
                name=customer_name,
                email=customer_email
            )
            print(f"Customer {customer_id} updated on Stripe")
        except stripe.error.InvalidRequestError:
            print(f"Customer {customer_id} not found on Stripe")
        except Exception as e:
            print(f"Error updating customer {customer_id} on Stripe: {e}")

    elif action == CUSTOMER_DELETED_EVENT:
        try:
            stripe.Customer.delete(customer_id)
            print(f"Customer {customer_id} deleted on Stripe")
        except stripe.error.InvalidRequestError:
            print(f"Customer {customer_id} not found on Stripe")
        except Exception as e:
            print(f"Error deleting customer {customer_id} on Stripe: {e}")

def main():
    try:
        while True:
            msg = kafka_consumer.poll(1.0)
            print("Polling")
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('End of partition reached')
                else:
                    print(f'Error while consuming message: {msg.error()}')
            else:
                print(f'Received message: {msg.value()}')
                check_event(msg)
            kafka_consumer.commit()
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        kafka_consumer.close()
        print("Consumer closed")

if __name__ == "__main__":
    main()