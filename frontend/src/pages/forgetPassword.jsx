
import React from 'react';
import { Container, Typography, Button, Box, Link } from '@mui/material';
import ForgetPasswordForm from '../components/ForgetPasswordForm';

const ForgetPassword = () => {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Forget Password
      </Typography>
      <ForgetPasswordForm />
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
    </Container>
  );
};

export default ForgetPassword;
