import React from 'react';
import { Button, Typography, Container, Box, Paper } from '@mui/material';
import Login from '../components/LoginForm';
import SignUpForm from '../components/SignUpForm';
import { Link } from 'react-router-dom';
import { API_URL } from '../config';


const Home = () => {
  const googleAuthLink = `${API_URL}/user/google-auth-redirect`;
  return (
    <Container maxWidth="sm" sx={{ py: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Welcome
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3, mt: 3, justifyContent: 'center', alignItems: 'center' }}>
        <Box sx={{ flex: 1, maxWidth: '300px', width: '100%' }}>
          <Login />
        </Box>
        <Box sx={{ flex: 1, maxWidth: '300px', width: '100%' }}>
          <SignUpForm />
        </Box>
      </Box>
      <Box sx={{ mt: 3 }}>
        <Button
          variant="contained"
          color="secondary"
          fullWidth
          sx={{ py: 1.5 }}
        >
          <Link to={googleAuthLink} target="_blank" rel="noopener noreferrer">
            Register with Google
          </Link>
        </Button>
      </Box>
    </Container>
  );
};

export default Home;