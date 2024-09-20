
import React from 'react';
import SendVerificationLinkForm from '../components/SendVerificationLinkForm';
import { Container, Typography, Box, Button, Link } from '@mui/material';

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

export default SendVerificationLink;
