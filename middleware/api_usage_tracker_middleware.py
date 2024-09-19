import re
from django.http import JsonResponse
from utils.api_exception import ApiException
from rest_framework.response import Response
from event.models import Event, EventAttendee
from muta_event.settings import SUBSCRIPTION_CONFIG

uuid_pattern = re.compile(r'[0-9a-fA-F-]{36}')

def create_event_handler(request, *arg, **kwargs):
    total_events = None
    try:
        total_events = Event.objects.filter(organizer=request.muta_user).count()
    except Exception as e:
        raise ApiException("Error while fetching total events", 500)
    
    if total_events >= SUBSCRIPTION_CONFIG['FREE']['max_events']:
        raise ApiException("You have reached the maximum number of events", 403)
    
    return None

def register_attendee_handler(request, *arg, **kwargs):
    total_attendees = None
    event_id = None
    match = re.search(uuid_pattern, request.path)

    if match:
        event_id = match.group(0)
    else:
        raise ApiException("Invalid event id", 400)
    
    try:
        total_attendees = EventAttendee.objects.filter(event_id=event_id).count()
    except Exception as e:
        raise ApiException("Error while fetching total attendees", 500)
    
    if total_attendees >= SUBSCRIPTION_CONFIG['FREE']['max_attendees_per_event']:
        raise ApiException("You have reached the maximum number of attendees", 403)
    
    return None

api_endpoints = {
    'create-event': ('/event/create-event', create_event_handler),
    'register-event': ('^/event/register-event/[0-9a-fA-F-]{36}$', register_attendee_handler),
}

class ApiUsageTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request, *args, **kwds):
        response = Response()
        for endpoint_name, endpoint_info in api_endpoints.items():
            if re.match(endpoint_info[0], request.path):
                try:
                    endpoint_info[1](request, *args, **kwds)
                except ApiException as e:
                    return JsonResponse({"message": e.message}, status=e.status_code)
                except Exception as e:
                    return JsonResponse({"message": "Internal Server Error"}, status=500)
                
        return self.get_response(request,*args, **kwds)