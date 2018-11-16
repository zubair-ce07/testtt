import React from 'react';
import { string } from 'prop-types';

const CardDescription = ({ description }) => {
  return <p className="card-text player-description">{description}</p>;
};

CardDescription.propTypes = {
  description: string
};

export default CardDescription;
