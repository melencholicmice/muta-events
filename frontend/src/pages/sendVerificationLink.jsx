
import React from 'react';
import SendVerificationLinkForm from '../components/SendVerificationLinkForm';
import { Container, Typography, Box } from '@mui/material';

const SendVerificationLink = () => {
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
          Send Verification Link
        </Typography>
        <SendVerificationLinkForm />
      </Box>
    </Container>
  );
};

export default SendVerificationLink;
