import React, { useEffect, useState } from 'react';
import { Box, Typography, Avatar, Container, Button, Link } from '@mui/material';
import { styled } from '@mui/system';
import UserInfoSection from '../components/UserInfoSection';
import { EventList } from '../components/displayEventSection';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { API_URL } from '../config';

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
  const navigate = useNavigate();

  const [userData, setUserData] = useState(null);
  useEffect(() => {
    const fetchUserData = async (token) => {
      if(token){
        localStorage.setItem('token', token);   
      }
      token = localStorage.getItem('token');
      if(!token) {
          const authCookie = document.cookie.split('; ').find(row => row.startsWith('Authorization='));
          console.log(authCookie)
          if (!authCookie) {
            toast.error('Please login to view this page');
            navigate('/home');
            return;
          }
      }

      try {
        const response = await fetch(`${API_URL}/user/get-user-data`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.status != 200) {
          throw new Error('Failed to fetch user data');
        }
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.log(error)
        toast.error('Error fetching user data:', error);
        navigate('/home');
      }
    };

    fetchUserData(token);
  }, [navigate]);

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
        {userData ? (<EventList token={token} sub={userData.subscription_type}/>) : (<>Loading....</>)}
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
