from rest_framework.views import APIView
from event.models import (
    Event,
    EventAttendee
)
from rest_framework.response import Response


class CreateEvent(APIView):
    def __init__(self):
        ...

    def post(self, request):
        response = Response()
        event = None
        try:
            event = Event.objects.create(
                name=request.data['name'],
                description=request.data['description'],
                location=request.data['location'],
                organizer=request.user
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

    def post(self, request):
        response = Response()
        event = None
        attendee = None
        try:
            event = Event.objects.get(event_id=request.data['event_id'])
            attendee = EventAttendee.create(
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
            event = Event.objects.get(event_id=request.data['event_id'])
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
            events = Event.objects.filter(organizer=request.user)
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
            attendees = EventAttendee.objects.filter(event=event).values('user__id', 'user__username', 'user__email')
        except Exception as e:
            response.data = {"message":"Attendees not found"}
            response.status_code = 500
            return response
        
        response.data = {
            "message":"Attendees found",
            "data": attendees
        }
        response.status_code = 200
        return response
        