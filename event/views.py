import stripe
from rest_framework.views import APIView
from event.models import (
    Event,
    EventAttendee
)
from middleware.validator import ValidateSchema
from event.schema import (
    CreateEventSchema,
    RegisterAttendeeSchema,
    EditBoughtEventSchema
)
from django.http import JsonResponse
from user.models import User , SubscriptionEnum
from rest_framework.response import Response
from muta_event.settings import FRONTEND_URL, STRIPE_SECRET_KEY
from django.shortcuts import redirect

stripe.api_key = STRIPE_SECRET_KEY

class CreateEvent(APIView):
    def __init__(self):
        ...

    @ValidateSchema(CreateEventSchema)
    def post(self, request):
        response = Response()
        event = None
        try:
            event = Event.objects.create(
                name=request.data['name'],
                description=request.data['description'],
                location=request.data['location'],
                organizer=request.muta_user
            )
            event.save()
        except Exception as e:
            response.data = {"message":"Event creation failed"}
            response.status_code = 500
            return response
        
        response.data = {
            "message":"Event created successfully",
            "data": {
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
                "organizer":event.organizer.first_name + " " + event.organizer.last_name,
            }
        }
        response.status_code = 200
        return response

class RegisterAttendee(APIView):
    def __init__(self):
        ...
    @ValidateSchema(RegisterAttendeeSchema)
    def post(self, request, event_id):
        response = Response()
        event = None
        attendee = None
        try:
            event = Event.objects.get(event_id=event_id)
            attendee = EventAttendee.objects.create(
                event=event,
                name=request.data['name'],
                phone_number=request.data['phone_number'],
                email=request.data['email']
            )
            attendee.save()
        except Exception as e:
            response.data = {"message":"Attendee registration failed"}
            response.status_code = 500
            return response

        response.data = {
            "message":"Attendee registered successfully",
            "data": {
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
            }
        }
        response.status_code = 200
        return response
    
class GetEvent(APIView):
    def __init__(self):
        ...
    
    def get(self, request, event_id):
        response = Response()
        event = None
        try:
            event = Event.objects.get(event_id=event_id)
        except Exception as e:
            response.data = {"message":"Event not found"}
            response.status_code = 500
            return response
        
        response.data = {
            "message":"Event found",
            "data": {
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
                "is_bought":event.is_bought,
            }
        }
        response.status_code = 200
        return response
    
class GetAllEventsByUser(APIView):
    def __init__(self):
        ...

    def get(self, request):
        response = Response()
        events = None
        try:
            events = Event.objects.filter(organizer=request.muta_user)
        except Exception as e:
            response.data = {"message":"Events not found"}
            response.status_code = 500
            return response

        events_data = []
        for event in events:
            events_data.append({
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
                "is_bought":event.is_bought,
            })
            
        response.data = {
            "message":"Events found",
            "data": events_data
        }
        response.status_code = 200
        return response
    

class GetAllAttendeesByEvent(APIView):
    def __init__(self):
        ...
    
    def get(self, request, event_id):
        response = Response()
        event = None
        attendees = None
        try:
            event = Event.objects.get(event_id=event_id)
            attendees = EventAttendee.objects.filter(event=event).values('name', 'email', 'phone_number', 'created_at')
        except Exception as e:
            response.data = {"message":"Attendees not found"}
            response.status_code = 500
            return response
        
        response.data = {
            "message":"Attendees found",
            "event_id": str(event.event_id),
            "data": attendees
        }
        response.status_code = 200
        return response
    
class GetAllBoughtEvents(APIView):
    def __init__(self):
        ...

    def get(self, request):
        response = Response()
        events = None
        base_url = request.build_absolute_uri('/')
        try:
            events = Event.objects.filter(organizer=request.muta_user, is_bought=True)  
        except Exception as e:
            response.data = {"message":"Events not found"}
            response.status_code = 500
            return response
        
        events_data = []
        for event in events:
            events_data.append({
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
                "edit_link": base_url + f"event/edit-bought-event/{event.event_id}"
            })
        
        response.data = {
            "message":"Events found",
            "data": events_data
        }
        response.status_code = 200
        return response
    
class EditBoughtEvent(APIView):
    def __init__(self):
        ...
    @ValidateSchema(EditBoughtEventSchema)
    def post(self, request, event_id):
        response = Response()
        event = None
        try:
            event = Event.objects.get(event_id=event_id)
        except Exception as e:
            response.data = {"message":"Event not found"}
            response.status_code = 500
            return response
        
        if not event:
            response.data = {"message":"Event not found"}
            response.status_code = 500
            return response

        if not ((event.is_bought == True) or (request.muta_user.subscription == SubscriptionEnum.PREMIUM.internal)):
            response.data = {"message":"Event is not editable, either it is not bought or you are not a premium user"}
            response.status_code = 500
            return response
        
        name = request.data.get('name')
        description = request.data.get('description')
        location = request.data.get('location')

        if name:
            event.name = name
        if description:
            event.description = description
        if location:
            event.location = location

        event.save()
        response.data = {
            "message":"Event found",
            "data": {
                "event_id": str(event.event_id),
                "name":event.name,
                "description":event.description,
                "location":event.location,
            }
        }
        
        response.status_code = 200
        return response
        
def buy_single_event(request):
    checkout_session = None
    base_url = request.build_absolute_uri('/')
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1Q0sLcP01A1kBUrC9LvOLWXl',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url= base_url + 'event/get-all-bought-events',
            cancel_url= FRONTEND_URL + '?canceled=true',
        )
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Payment failed"}, status=500)

    if not checkout_session:
        JsonResponse({"message":"Payment failed"}, status=500)
    
    return redirect(checkout_session.url, code=303)

