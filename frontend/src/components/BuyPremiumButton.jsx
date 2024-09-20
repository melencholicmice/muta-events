
import React from 'react';
import { Button, Link } from '@mui/material';
import { API_URL } from '../config';

const BuyPremiumButton = ({ isPremium }) => {
  return (
    <Button
      variant="contained"
      color="primary"
    >
      {isPremium ? (
        <Link href={`${API_URL}/user/buy-premium-subscription`}  color="inherit" underline="none">
          Upgrade to Premium
        </Link>
      ) : (
        "You're a Premium User"
      )}
    </Button>
  );
};

export default BuyPremiumButton;
