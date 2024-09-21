# MUTA EVENT 🎉

## Overview 🌟
MUTA EVENT is an event management and registration platform built using Django REST Framework and PostgreSQL.

## Subscription Plans 💼

The MUTA EVENT application offers the following subscription plans:

### Free Plan 🆓
- **Max Events**: 3
- **Max Attendees per Event**: 3

This is the default plan for all users when they sign up. It allows users to create up to 3 events and have a maximum of 3 attendees per event.

### Premium Plan 🌟
- **Max Events**: No limit
- **Max Attendees per Event**: No limit

To purchase the premium plan, users can use the `/user/buy-premium-subscription` endpoint, as mentioned in the README.md file.

## Tech Stack 🛠️

The MUTA EVENT project uses the following technologies:

- **Django REST Framework (DRF)**: Core framework for building the backend API
- **PostgreSQL**: Robust database backend
- **Celery**: Distributed task queue system for asynchronous processing
- **RabbitMQ**: Message broker for Celery
- **React.js**: Frontend library for building user interfaces
- **React Google reCAPTCHA**: CAPTCHA verification for user actions
- **Vite**: Fast build tool for React frontend
- **Stripe**: Payment processing platform
- **Google OAuth2**: Authentication using Google accounts

## API Endpoints 🚀

### 1. User Management 👤

#### 1.1. User Login
- **Endpoint:** `/user/sign-in`
- **Method:** POST
- **Description:** Allows users to log in to the application

#### 1.2. User Signup
- **Endpoint:** `/user/sign-up`
- **Method:** POST
- **Description:** Allows users to register for the application

#### 1.3. Forget Password
- **Endpoint:** `/user/forget-password`
- **Method:** POST
- **Description:** Allows users to request a password reset

#### 1.4. Reset Password
- **Endpoint:** `/user/reset-password`
- **Method:** POST
- **Description:** Allows users to reset their password

#### 1.5. Verify Email
- **Endpoint:** `/user/verify-email`
- **Method:** GET
- **Description:** Allows users to verify their email address

#### 1.6. Send Verification Link
- **Endpoint:** `/user/send-verification-link`
- **Method:** POST
- **Description:** Allows users to request a new email verification link

#### 1.7. Get User Data
- **Endpoint:** `/user/get-user-data`
- **Method:** GET
- **Description:** Allows users to retrieve their profile information

#### 1.8. Google Auth Redirect
- **Endpoint:** `/user/google-auth-redirect`
- **Method:** GET
- **Description:** Redirects the user to the Google OAuth2 authorization flow

#### 1.9. Google Auth Callback
- **Endpoint:** `/user/google-auth-callback`
- **Method:** GET
- **Description:** Handles the callback from the Google OAuth2 authorization flow

#### 1.10. Buy Premium Subscription
- **Endpoint:** `/user/buy-premium-subscription`
- **Method:** GET
- **Description:** Allows users to purchase a premium subscription

### 2. Event Management 📅

#### 2.1. Create Event
- **Endpoint:** `/event/create-event`
- **Method:** POST
- **Description:** Allows users to create a new event

#### 2.2. Register Attendee
- **Endpoint:** `/event/register-event/{event_id}`
- **Method:** POST
- **Description:** Allows users to register as an attendee for an event

#### 2.3. Get Event
- **Endpoint:** `/event/get-event/{event_id}`
- **Method:** GET
- **Description:** Allows users to retrieve the details of a specific event

#### 2.4. Get All Events by User
- **Endpoint:** `/event/get-all-events-by-user`
- **Method:** GET
- **Description:** Allows users to retrieve a list of all events they have created

#### 2.5. Get All Attendees by Event
- **Endpoint:** `/event/get-all-attendees-by-event/{event_id}`
- **Method:** GET
- **Description:** Allows users to retrieve a list of all attendees for a specific event

#### 2.6. Buy Single Event
- **Endpoint:** `/event/buy-single-event`
- **Method:** GET
- **Description:** Allows users to purchase a single event

#### 2.7. Get All Bought Events
- **Endpoint:** `/event/get-all-bought-events`
- **Method:** GET
- **Description:** Allows users to retrieve a list of all events they have purchased

#### 2.8. Edit Bought Event
- **Endpoint:** `/event/edit-bought-event/{event_id}`
- **Method:** POST
- **Description:** Allows users to edit the details of an event they have purchased

## Middleware 🔒

The application includes two middleware classes:

1. **UserAuthMiddleware**: Handles user authentication and protects certain API endpoints
2. **ApiUsageTrackerMiddleware**: Tracks the usage of the API

These middleware classes are integrated into the overall application flow and do not have dedicated endpoints.