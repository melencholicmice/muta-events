
import React from 'react';
import { Link } from 'react-router-dom';
import { API_URL } from '../config';

const BuyEventButton = ({ isAvailable, eventId }) => {
  return (
    <>
      {isAvailable ? (
        <Link to={`${API_URL}/event/buy-single-event`} className="btn btn-primary">
          Buy Event
        </Link>
      ) : (
        <span className="text-muted">You are Premium no need to buy!!</span>
      )}
    </>
  );
};

export default BuyEventButton;
