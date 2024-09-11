from confluent_kafka import Consumer, KafkaError
import stripe
import json

CUSTOMER_CREATED_EVENT = 'customer_created'
CUSTOMER_DELETED_EVENT = 'customer_deleted'

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
    if message['action'] == CUSTOMER_CREATED_EVENT:
        try:
            stripe.Customer.create(
                id=message['customer_id'],
                name=message['customer_name'],
                email=message['customer_email']
            )
            print(f"Customer {message['customer_id']} created on stripe")    
        except:
            print(f"Customer {message['customer_id']} error on stripe")
    

    elif message['action'] == CUSTOMER_DELETED_EVENT:
        try:
            stripe.Customer.delete(str(message['customer_id']))
            print(f"Customer {message['customer_id']} deleted")
        except stripe.error.InvalidRequestError:
            print(f"Customer {message['customer_id']} not found in Stripe")


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