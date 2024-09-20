
import React from 'react';
import ResetPasswordForm from '../components/ResetPasswordForm';
import { Container, Typography, Box } from '@mui/material';

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
    </Container>
  );
};

export default ResetPassword;
