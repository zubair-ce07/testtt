import React from 'react';
import { string } from 'prop-types';

const CardTitle = ({ title }) => {
  return <h4 className="card-title player-title">{title}</h4>;
};

CardTitle.propTypes = {
  title: string
};

export default CardTitle;
