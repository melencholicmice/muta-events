
import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Box, Typography, CircularProgress } from '@mui/material';
import { API_URL } from '../config';

const ShowEvent = ({event_id, name, description, location}) => {
  return (
    <Box p={3}>
      {name && description ? (
        <>
          <Typography variant="h4" gutterBottom>Name: {name}</Typography>
          <Typography variant="body1">Description: {description}</Typography>
          <Typography variant="body2">Event ID:{event_id} </Typography>
          <Typography variant="body2">Location: {location}</Typography>
        </>
      ) : (
        <Typography>No event data available</Typography>
      )}
    </Box>
  );
};

export default ShowEvent;
