from rest_framework.views import APIView
from event.models import (
    Event,
    EventAttendee
)
from middleware.validator import ValidateSchema
from event.schema import (
    CreateEventSchema,
    RegisterAttendeeSchema,
)
from rest_framework.response import Response


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
        