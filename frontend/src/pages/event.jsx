import React, { useState, useEffect } from 'react';
import { Box, Container, CircularProgress, Link, Button } from '@mui/material';
import ShowEvent from '../components/ShowEvent';
import { useLocation, useNavigate } from 'react-router-dom';
import { API_URL } from '../config';
import { AttendeeList } from '../components/showAttendees';

const EventPage = () => {
  const [eventData, setEventData] = useState(null);
  const location = useLocation();
  const navigator = useNavigate();
  const params = new URLSearchParams(location.search);
  const event_id = params.get('event_id');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
      const fetchEventData = async () => {
          try {
              const token = localStorage.getItem('token');
              if(!token){
                navigator('/home')
              }
              const response = await fetch(`${API_URL}/event/get-event/${event_id}`, {
                  headers: {
                      'Authorization': `Bearer ${token}`
                  }
              });
              if (response.status === 200) {
                  const data = await response.json();
                  setEventData(data.data);
                  setLoading(false);
              } else {
                  throw new Error(`Failed to load event data: ${response.status}`);
              }
          } catch (err) {
              setError(err.message);
              setLoading(false);
          }
      };

      fetchEventData();
  }, [event_id]);

  if (loading) {
      return (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
              <CircularProgress />
          </Box>
      );
  }

  if (error) {
      return (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
              <p>{error}</p>
          </Box>
      );
  }
    
  return (
      <Box
          sx={{
              display: 'flex',
              flexDirection:'column',
              justifyContent: 'center',
              alignItems: 'center',
              minHeight: '100vh',
              backgroundColor: '#f5f5f5',
          }}
      >
          <Container maxWidth="md">
              <Box
                  sx={{
                      backgroundColor: 'white',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                      padding: '24px',
                      marginBottom: '24px',
                  }}
              >
                  <ShowEvent event_id={event_id} name={eventData.name} description={eventData.description} location={eventData.location}/>
              </Box>
          </Container>
          <Container maxWidth="md">
              <Box
                  sx={{
                      backgroundColor: 'white',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                      padding: '24px',
                  }}
              >
                <AttendeeList event_id={event_id} />
              </Box>
          </Container>
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
      </Box>
  );
};

export default EventPage;
