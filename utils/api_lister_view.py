from django.http import JsonResponse

def list_api(request):
    api_details = [
        {
            "category": "User Management",
            "description": "Endpoints related to user authentication, registration, and profile management",
            "endpoints": [
                {
                    "name": "User Login",
                    "endpoint": "/user/sign-in",
                    "method": "POST",
                    "description": "Allows users to log in to the application",
                    "required_fields": ["email", "password"],
                    "response": "Returns a JWT token for authentication"
                },
                {
                    "name": "User Signup",
                    "endpoint": "/user/sign-up",
                    "method": "POST",
                    "description": "Allows users to register for the application",
                    "required_fields": ["first_name", "last_name", "email", "password", "recaptcha"],
                    "response": "Returns a success message and sends a verification email"
                },
                {
                    "name": "Forget Password",
                    "endpoint": "/user/forget-password",
                    "method": "POST",
                    "description": "Allows users to request a password reset",
                    "required_fields": ["email"],
                    "response": "Sends a password reset link to the user's email"
                },
                {
                    "name": "Reset Password",
                    "endpoint": "/user/reset-password",
                    "method": "POST",
                    "description": "Allows users to reset their password",
                    "required_fields": ["token", "new_password"],
                    "response": "Returns a success message upon password reset"
                },
                {
                    "name": "Verify Email",
                    "endpoint": "/user/verify-email",
                    "method": "GET",
                    "description": "Allows users to verify their email address",
                    "required_params": ["token"],
                    "response": "Confirms email verification and redirects to login page"
                },
                {
                    "name": "Send Verification Link",
                    "endpoint": "/user/send-verification-link",
                    "method": "POST",
                    "description": "Allows users to request a new email verification link",
                    "required_fields": ["email"],
                    "response": "Sends a new verification link to the user's email"
                },
                {
                    "name": "Get User Data",
                    "endpoint": "/user/get-user-data",
                    "method": "GET",
                    "description": "Allows users to retrieve their profile information",
                    "authentication": "Requires valid JWT token",
                    "response": "Returns user profile data"
                },
                {
                    "name": "Google Auth Redirect",
                    "endpoint": "/user/google-auth-redirect",
                    "method": "GET",
                    "description": "Redirects the user to the Google OAuth2 authorization flow",
                    "response": "Redirects to Google login page"
                },
                {
                    "name": "Google Auth Callback",
                    "endpoint": "/user/google-auth-callback",
                    "method": "GET",
                    "description": "Handles the callback from the Google OAuth2 authorization flow",
                    "required_params": ["code"],
                    "response": "Logs in the user and returns a JWT token"
                },
                {
                    "name": "Buy Premium Subscription",
                    "endpoint": "/user/buy-premium-subscription",
                    "method": "GET",
                    "description": "Allows users to purchase a premium subscription",
                    "authentication": "Requires valid JWT token",
                    "response": "Redirects to payment gateway"
                }
            ]
        },
        {
            "category": "Event Management",
            "description": "Endpoints related to creating, managing, and purchasing events",
            "endpoints": [
                {
                    "name": "Create Event",
                    "endpoint": "/event/create-event",
                    "method": "POST",
                    "description": "Allows users to create a new event",
                    "authentication": "Requires valid JWT token",
                    "required_fields": ["name", "description", "location"],
                    "response": "Returns created event details"
                },
                {
                    "name": "Register Attendee",
                    "endpoint": "/event/register-event/{event_id}",
                    "method": "POST",
                    "description": "Allows users to register as an attendee for an event",
                    "authentication": "Requires valid JWT token",
                    "required_params": ["event_id"],
                    "required_fields": ["name", "email", "phone_number"],
                    "response": "Returns registration confirmation"
                },
                {
                    "name": "Get Event",
                    "endpoint": "/event/get-event/{event_id}",
                    "method": "GET",
                    "description": "Allows users to retrieve the details of a specific event",
                    "required_params": ["event_id"],
                    "response": "Returns event details"
                },
                {
                    "name": "Get All Events by User",
                    "endpoint": "/event/get-all-events-by-user",
                    "method": "GET",
                    "description": "Allows users to retrieve a list of all events they have created",
                    "authentication": "Requires valid JWT token",
                    "response": "Returns a list of events created by the user"
                },
                {
                    "name": "Get All Attendees by Event",
                    "endpoint": "/event/get-all-attendees-by-event/{event_id}",
                    "method": "GET",
                    "description": "Allows users to retrieve a list of all attendees for a specific event",
                    "authentication": "Requires valid JWT token",
                    "required_params": ["event_id"],
                    "response": "Returns a list of attendees for the specified event"
                },
                {
                    "name": "Buy Single Event",
                    "endpoint": "/event/buy-single-event",
                    "method": "GET",
                    "description": "Allows users to purchase a single event",
                    "authentication": "Requires valid JWT token",
                    "required_params": ["event_id"],
                    "response": "Redirects to payment gateway for event purchase"
                },
                {
                    "name": "Get All Bought Events",
                    "endpoint": "/event/get-all-bought-events",
                    "method": "GET",
                    "description": "Allows users to retrieve a list of all events they have purchased",
                    "authentication": "Requires valid JWT token",
                    "response": "Returns a list of events purchased by the user"
                },
                {
                    "name": "Edit Bought Event",
                    "endpoint": "/event/edit-bought-event/{event_id}",
                    "method": "POST",
                    "description": "Allows users to edit the details of an event they have purchased",
                    "authentication": "Requires valid JWT token",
                    "required_params": ["event_id"],
                    "required_fields": ["name", "description", "location"],
                    "response": "Returns updated event details"
                }
            ]
        }
    ]

    return JsonResponse({
        "message": "Hello from muta events, here you can make get info of all apis",
        "Important" : " please note that this is just a testing deployment so some features might not work, to access complete applicatoin build from source :- https://github.com/melencholicmice/muta-events  ",
        "api_details":api_details,   
    },safe=False)