import React, { useState } from "react";
import { TextField, Button, Container, Box } from "@mui/material";
import { API_URL } from "../config";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Link } from 'react-router-dom';

const CreateEventForm = () => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [location, setLocation] = useState("");
    const [nameError, setNameError] = useState(false);
    const [descriptionError, setDescriptionError] = useState(false);
    const [locationError, setLocationError] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        setNameError(false);
        setDescriptionError(false);
        setLocationError(false);

        const token = localStorage.getItem('token');

        if (!token) {
            toast.error('Please login to create an event');
            return;
        }

        if (name === '') {
            setNameError(true);
        }
        if (description === '') {
            setDescriptionError(true);
        }
        if (location === '') {
            setLocationError(true);
        }

        if (name && description && location) {
            fetch(`${API_URL}/event/create-event`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ 
                    "name": name, 
                    "description": description,
                    "location": location
                }),
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
                toast.success('Event created successfully!');
            })
            .catch((error) => {
                console.error('Error:', error);
                toast.error(error);
            });
        }
    };

    return (
        <Container maxWidth="sm">
            <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <h2>Create Event</h2>

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="name"
                    label="Event Name"
                    name="name"
                    autoFocus
                    onChange={e => setName(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={name}
                    error={nameError}
                    helperText={nameError ? "Event name is required" : ""}
                />

                <TextField
                    margin="normal"
                    required
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
                    error={descriptionError}
                    helperText={descriptionError ? "Description is required" : ""}
                />

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="location"
                    label="Location"
                    name="location"
                    onChange={e => setLocation(e.target.value)}
                    variant="outlined"
                    color="secondary"
                    value={location}
                    error={locationError}
                    helperText={locationError ? "Location is required" : ""}
                />

                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    color="secondary"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Create Event
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

export default CreateEventForm;