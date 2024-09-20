
import React from 'react';
import { Container, Typography } from '@mui/material';
import ForgetPasswordForm from '../components/ForgetPasswordForm';

const ForgetPassword = () => {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        Forget Password
      </Typography>
      <ForgetPasswordForm />
    </Container>
  );
};

export default ForgetPassword;
