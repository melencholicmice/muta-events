
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Typography, Box } from '@mui/material';
import { API_URL } from '../config';
import { toast } from 'react-toastify';

const SendVerificationLinkFrom = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setError('');
      setLoading(true);
          const response = await fetch(`${API_URL}/user/send-verification-link`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
          });
          
          const data = await response.json();
          
          if (response.status === 200) {
            toast.success(data.message);
            navigate('/home');
          } else {
            toast.error(data.message || 'Failed to send password reset email');
          }
    } catch {
      setError('Failed to reset password');
    }
    setLoading(false);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <Typography variant="h5" component="h1" gutterBottom>
        Enter your email to send verification link
      </Typography>
    
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        autoFocus
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
        disabled={loading}
      >
        Send Verification Email
      </Button>
    </Box>
  );
};

export default SendVerificationLinkFrom;
