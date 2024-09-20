import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Box, Link, Container, Button } from '@mui/material';
import { API_URL } from '../config';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const EventListItem = ({ id, name, is_bought }) => {
  return (
    <ListItem sx={{ border: '1px solid #ccc', borderRadius: '4px', mb: 2, padding: '16px' }}>
      <ListItemText
        primary={
          <Typography align="left">
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="1.2rem" 
              mr={1}
            > 
                <Link 
                href={`/event?event_id=${id}`} 
                sx={{ 
                  fontSize: '1.2rem',
                  '&:hover': {
                    textDecoration: 'underline'
                    }
                }}
                >
                {name}
                </Link>
            </Box>
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="1.2rem" 
              mr={1}
            >
              {id} 
            </Box>
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="1.2rem" 
              mr={1}
            >
               {is_bought ? (
                    <Link
                    href={`/edit-event?event_id=${id}`}
                    target="_blank" 
                    rel="noopener noreferrer"
                    >
                      edit
                    </Link>
               ) : <>buy subscription to edit</>}
            </Box>
          </Typography>
        }
      />
    </ListItem>
  );
};

const EventList = ({token}) => {
  const [events, setEvents] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvents = async () => {
        console.log("trying to fetch events");
      try {
        if(localStorage.getItem('token') === null){
            localStorage.setItem('token', token);
        }

        const response = await fetch(`${API_URL}/event/get-all-events-by-user`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          const data = await response.json();
          setEvents(data.data);
        }
        else{
            throw new Error('Failed to fetch events');
        }
      } catch (error) {
        toast.error(error);
      }
    };

    fetchEvents();
  }, []);
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>Event List</Typography>
        <List sx={{ width: '100%' }}>
          {events.map((event) => (
            <EventListItem key={event.id} id={event.event_id} name={event.name} is_bought={event.is_bought} />
          ))}
        </List>
      </Box>
    </Container>
  );
};

export { EventListItem, EventList };