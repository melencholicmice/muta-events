
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ShowEvent from '../components/ShowEvent';
import { API_URL } from '../config';
import { toast } from 'react-toastify';
import EventRegistrationForm from '../components/EventRegistrationForm';
import { Button, Box, Link } from '@mui/material';

const RegisterEvent = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const event_id = params.get('event_id');
  const [event, setEvent] = useState(null);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        await fetch(`${API_URL}/event/get-event/${event_id}`,{
            method:'GET',
            headers:{
                'Content-Type': 'application/json',
            },
            credentials:'include',
        })
        .then(response => {
            if (response.status !== 200){
                return response.json().then( data => {
                    throw new Error(data.message || 'Network response was not ok');
                });
            }
            return response.json();
        })
        .then(data => {
            setEvent(data.data);
            console.log(data);
        })
        .catch((error) => {
            console.log(error);
            toast.error(error);
        })

      } catch (error) {
        console.log(error);
        toast.error(error);
      }
    };

    fetchEvent();
  }, [event_id]);

  if (!event) {
    return <div>Loading...</div>;
  }

  return (
    <div className="register-event-page">
      <ShowEvent 
        event_id={event.event_id} 
        name={event.name} 
        description={event.description} 
        location={event.location}
      />
      <EventRegistrationForm event_id={event_id} />
      <Box sx={{ mt: 3 }}>
        <Button
          variant="contained"
          color="secondary"
          fullWidth
          sx={{ py: 1.5 }}
        >
          <Link to='/home' rel="noopener noreferrer">
            Home
          </Link>
        </Button>
      </Box>
    </div>
  );
};

export default RegisterEvent;
