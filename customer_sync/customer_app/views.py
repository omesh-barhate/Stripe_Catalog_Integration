from django.shortcuts import render
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer,hookserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CustomerReadWrite(generics.ListCreateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class CustomerReadWriteDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class hookdata(APIView):
    def post(self, request, format=None):
        print('Received Stripe webhook')
        hook_obj = hookserializer(data=request.data)
        if hook_obj.is_valid():
            event_id = hook_obj.validated_data['id']
            event_type = hook_obj.validated_data['type']
            customer_data = hook_obj.validated_data['data']
            print('Received Stripe webhook with id={} and type={}'.format(event_id, event_type))
            print(customer_data)
            if (event_type=='customer.created'):
                customer_id = customer_data['object']['id']
                customer_name = customer_data['object']['name']
                customer_email = customer_data['object']['email']

                if not Customer.objects.filter(id=customer_id).exists():
                    customer = Customer(id=customer_id, name=customer_name, email=customer_email)
                    customer.save()
                    print('Created customer with id={}'.format(customer_id))
                else:
                    print('Customer with id={} already exists'.format(customer_id))
                return Response(status=status.HTTP_200_OK)
            elif (event_type=='customer.deleted'):
                customer_id = customer_data['object']['id']

                if Customer.objects.filter(id=customer_id).exists():
                    customer = Customer.objects.get(id=customer_id)
                    customer.delete()
                    print('Deleted customer with id={}'.format(customer_id))
                else:
                    print('Customer with id={} does not exist'.format(customer_id))
                return Response(status=status.HTTP_200_OK)
            elif (event_type=='customer.updated'):
                customer_id = customer_data['object']['id']
                customer_name = customer_data.get('object', {}).get('name')
                customer_email = customer_data.get('object', {}).get('email')
                
                if Customer.objects.filter(id=customer_id).exists():
                    customer = Customer.objects.get(id=customer_id)
                    if customer_name:
                        customer.name = customer_name
                    if customer_email:
                        customer.email = customer_email
                    customer.save()
                    print(f'Updated customer with id={customer_id}')
                else:
                    print(f'Customer with id={customer_id} does not exist')
                
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(hook_obj.errors, status=status.HTTP_400_BAD_REQUEST)