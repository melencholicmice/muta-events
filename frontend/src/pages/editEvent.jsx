import React, { useState } from "react";
import { TextField, Button, Container, Box } from "@mui/material";
import { API_URL } from "../config";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const EditEventForm = () => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [location, setLocation] = useState("");
    const loc = useLocation();
    const searchParams = new URLSearchParams(loc.search);
    const eventId = searchParams.get('event_id');

    if (!eventId) {
        toast.error('Event ID is missing');
    }
    

    const handleSubmit = (event) => {
        event.preventDefault();
        const token = localStorage.getItem('token');

        if (!token) {
            toast.error('Please login to create an event');
            return;
        }

        const updatedFields = {};
        if (name) updatedFields.name = name;
        if (description) updatedFields.description = description;
        if (location) updatedFields.location = location;

        if (Object.keys(updatedFields).length > 0) {
            fetch(`${API_URL}/event/edit-bought-event/${eventId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(updatedFields),
                credentials: 'include',
            })
            .then(response => {
                if (response.status !== 200) {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Network response was not ok');
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
                toast.success('Event updated successfully!');
                
            })
            .catch((error) => {
                console.error('Error:', error);
                toast.error(error);
            });
        } else {
            toast.warning('No fields to update');
        }
    };

    return (
        <Container maxWidth="sm">
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <h2>Edit Event</h2>

                <TextField
                    margin="normal"
                    fullWidth
                    id="name"
                    label="Event Name"
                    name="name"
                    autoFocus
                    onChange={e => setName(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={name}
                />

                <TextField
                    margin="normal"
                    fullWidth
                    id="description"
                    label="Description"
                    name="description"
                    multiline
                    rows={4}
                    onChange={e => setDescription(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={description}
                />

                <TextField
                    margin="normal"
                    fullWidth
                    id="location"
                    label="Location"
                    name="location"
                    onChange={e => setLocation(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={location}
                />

                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="secondary"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Update Event
                </Button>
                <Button
                    component={Link}
                    to={`/event?event_id=${eventId}`}
                    fullWidth
                    variant="outlined"
                    color="secondary"
                    sx={{ mt: 1, mb: 2 }}
                >
                    Return to Event Data
                </Button>
                <Button
                    component={Link}
                    to="/profile"
                    fullWidth
                    variant="outlined"
                    color="secondary"
                    sx={{ mt: 1, mb: 2 }}
                >
                    Return to Profile
                </Button>
            </Box>
        </Container>
    );
};

export default EditEventForm;