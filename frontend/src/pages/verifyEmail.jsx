import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { API_URL } from '../config';

const VerifyEmail = () => {
  const [verificationStatus, setVerificationStatus] = useState('Verifying...');
  const location = useLocation()
  const searchParams = new URLSearchParams(location.search)
  const token = searchParams.get('token')
  const navigate = useNavigate();

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await fetch(`${API_URL}/user/verify-email?token=${token}`);
        if (response.status === 200) {
          setVerificationStatus('Email verified successfully!');
          setTimeout(() => navigate('/home'), 3000);
        } else {
          setVerificationStatus('Verification failed. Please try again.');
        }
      } catch (error) {
        console.error('Error verifying email:', error);
        setVerificationStatus('An error occurred. Please try again later.');
      }
    };

    verifyEmail();
  }, [token, navigate]);

  return (
    <div className="verify-email-container">
      <h2>Email Verification</h2>
      <p>{verificationStatus}</p>
    </div>
  );
};

export default VerifyEmail;
