import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config';
import { toast } from 'react-toastify';

const UserInfoSection = ({token}) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
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
        if (response.status !== 200) {
          throw new Error('Failed to fetch user data');
        }
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        toast.error('Error fetching user data:', error);
        navigate('/home');
      } finally {
        setLoading(false);
      }
    };

    fetchUserData(token);
  }, [navigate]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (!userData) {
    return null;
  }

  return (
    <Box
      sx={{
        backgroundColor: 'background.paper',
        borderRadius: 2,
        padding: 3,
        boxShadow: 1,
      }}
    >
      <Typography variant="h5" gutterBottom>
        User Information
      </Typography>
      <Typography>User ID: {userData.user_id}</Typography>
      <Typography>Name: {userData.name}</Typography>
      <Typography>Email: {userData.email}</Typography>
      <Typography>Subscription: {userData.subscription_type}</Typography>
    </Box>
  );
};

export default UserInfoSection;