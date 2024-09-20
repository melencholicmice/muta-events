import React from 'react';
import { Box, Typography, Avatar, Container, Button, Link } from '@mui/material';
import { styled } from '@mui/system';
import UserInfoSection from '../components/UserInfoSection';
import { EventList } from '../components/displayEventSection';
import BuyEventButton from '../components/BuyEventButton';
import BuyPremiumButton from '../components/BuyPremiumButton';

const ProfileContainer = styled(Container)(({ theme }) => ({
  marginTop: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: theme.spacing(4),
}));

const ProfileAvatar = styled(Avatar)(({ theme }) => ({
  width: theme.spacing(20),
  height: theme.spacing(20),
  marginBottom: theme.spacing(2),
}));

const ProfileInfo = styled(Box)(({ theme }) => ({
  textAlign: 'center',
  marginBottom: theme.spacing(3),
}));

const Profile = () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');

  return (
    <ProfileContainer maxWidth="sm">
      <ProfileInfo>
        <Typography variant="h4" gutterBottom>
          User Profile
        </Typography>
      </ProfileInfo>

      <Button
        variant="contained"
        color="primary"
        href="/create-event"
        size="large"
        sx={{ mt: 2, mb: 4 }}
      >
        Create Event
      </Button>
      <UserInfoSection token={token} />
      <Box sx={{ width: '100%', mt: 4 }}>
        <EventList token={token} />
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
    </ProfileContainer>
  );
};

export default Profile;
