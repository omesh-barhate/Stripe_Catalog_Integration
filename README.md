# Two Way Integrations

Video Presentation :- https://youtu.be/RVyU-pX1Kmc

## Overview

 A two-way integration system connecting a local customer catalog with Stripe and Salesforce.

  It uses Kafka for event queuing and Django for managing customer data.
  
   The setup includes Docker for containerization and Ngrok for webhook tunneling.

## Prerequisites

Ensure the following are installed on your machine:

- Docker
- Ngrok
- Python3

## Setup and Deployment

Follow these steps to set up and deploy the application:

### 1. Clone the Repository and Cd into it

### 2. Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate
```

### 3. Install Project Dependencies
```
pip install -r requirements.txt
```

### 4. Start Docker Containers
```
sudo docker compose up -d
```

### 5. Create Kafka Topic
```
sudo docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic customer_events
```

### 6. Apply Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the worker
```
python worker.py
```

### 8.Stripe Integration
Use your Stripe key in the worker.

### 9. Add a Webhook Tunnel
Use Ngrok to tunnel the webhook .
```
ngrok http http://localhost:8000
```

### 10. Start the Django Development Server
```
python manage.py runserver
```

### 11. Access the Django Application
Open your web browser and navigate to http://localhost:8000 to access the Django application.

## Project Extension for Salesforce Customers

To integrate Salesforce’s Customer Catalog with our system, we will create a module named `salesforce_integration.py` using the `simple-salesforce` library. This module will manage CRUD operations for Salesforce Contact records and map them to a `SalesforceCustomer` model in our application.

We will also develop API endpoints for creating, updating, retrieving, and deleting Salesforce customer records. These endpoints will ensure efficient interaction with Salesforce’s Contact object.

For asynchronous communication, we will establish Kafka topics such as `salesforce-customer-created`, `salesforce-customer-updated`, and `salesforce-customer-deleted`. A Kafka producer will publish Salesforce events to these topics, while a Kafka consumer will process the events to update local customer data.

Lastly, we’ll configure webhooks (if supported) to convert Salesforce events into Kafka messages and implement secure authentication for accessing Salesforce APIs. Testing will ensure integration with both Salesforce and Stripe is seamless, with logging and monitoring in place to handle errors and track events.

## Project Extension for other customers
To extend our integrations to support additional systems, we'll use a modular approach. We will develop separate modules for each new system, following the pattern established with Salesforce and Stripe integrations. Each module will be responsible for retrieving data from the external system, transforming it to match our product's data model, and publishing it to a Kafka topic.

For instance, to integrate an invoice catalog, we will create a module that pulls invoice data from our database and publishes it to a Kafka topic in the format required by the external system. Similarly, another module will fetch invoice data from the external system and publish it to a different Kafka topic, transforming the data to fit our product's model.

Once data from various systems is in Kafka topics, we'll aggregate it into a single topic using Kafka Streams. A worker will then consume this aggregated topic to update our product’s database with the latest customer and invoice information.

By maintaining this modular approach, each system integration remains distinct, ensuring flexibility and scalability as we extend support to more systems.


