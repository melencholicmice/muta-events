
import React from 'react';
import ResetPasswordForm from '../components/ResetPasswordForm';
import { Container, Typography, Box, Button, Link } from '@mui/material';

const ResetPassword = () => {
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Reset Password
        </Typography>
        <ResetPasswordForm />
      </Box>
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

export default ResetPassword;
