import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Box, Link, Container, Button } from '@mui/material';
import { API_URL } from '../config';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';


const AttendeeListItem = ({ created_at, name, email, phone }) => {
  return (
    <ListItem sx={{ border: '1px solid #ccc', borderRadius: '4px', mb: 2, padding: '4px' }}>
      <ListItemText
        primary={
          <Typography align="left">
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="0.7rem" 
              mr={1}
            > 
              Name : {name}
            </Box>
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="0.7rem" 
              mr={1}
            >center
              Email : {email} 
            </Box>
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="0.7rem" 
              mr={1}
            >
              phone : {phone} 
            </Box>
            <Box 
              component="div" 
              fontWeight="bold" 
              fontSize="0.7rem" 
              mr={1}
            >
              Created at: {created_at} 
            </Box>
          </Typography>
        }
      />
    </ListItem>
  );
};

const AttendeeList = ({event_id}) => {
  const [attendees, setAttendees] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        if(localStorage.getItem('token') === null){
            localStorage.setItem('token', token);
        }

        const response = await fetch(`${API_URL}/event/get-all-attendees-by-event/${event_id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          const data = await response.json();
          setAttendees(data.data);
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
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>Attendee List</Typography>
        <List sx={{ width: '100%' }}>
            {
            attendees.length > 0 ? (
                attendees.map((attendee, ind) => (
                    <AttendeeListItem key={ind} created_at={attendee.created_at} name={attendee.name} email={attendee.email} phone={attendee.phone_number}/>
                ))
            ) : (
                <Typography variant="h6" align="center" sx={{ mt: 4 }}>
                    No attendees found for this event.
                </Typography>
            )
        }
        </List>
      </Box>
    </Container>
  );
};

export { AttendeeListItem, AttendeeList };