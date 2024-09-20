
import React from 'react';
import { Box, Typography, Avatar, Container } from '@mui/material';
import { styled } from '@mui/system';
import UserInfoSection from '../components/UserInfoSection';

const ProfileContainer = styled(Container)(({ theme }) => ({
  marginTop: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
}));

const ProfileAvatar = styled(Avatar)(({ theme }) => ({
  width: theme.spacing(20),
  height: theme.spacing(20),
  marginBottom: theme.spacing(2),
}));

const ProfileInfo = styled(Box)(({ theme }) => ({
  textAlign: 'center',
}));

const Profile = () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');

  return (
    <ProfileContainer maxWidth="sm">
      <UserInfoSection token={token}/>
        <Typography variant="h4" gutterBottom>
          John Doe
        </Typography>
        <Typography variant="body1" color="textSecondary" paragraph>
          Software Developer
        </Typography>
        <Typography variant="body2" paragraph>
          Passionate about creating innovative solutions and learning new technologies.
        </Typography>
        <Typography variant="body2">
          Email: john.doe@example.com
        </Typography>
        <Typography variant="body2">
          Location: San Francisco, CA
        </Typography>
    </ProfileContainer>
  );
};

export default Profile;
