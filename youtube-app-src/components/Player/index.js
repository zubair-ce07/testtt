import React from 'react';
import * as constants from '../../shared/constants.js';
import CardTitle from './cardTitle.js';
import CardDescription from './cardDescription.js';
import Iframe from './iframe.js';

const Player = props => {
  if (!props.source) return null;

  const {
    source: { title, description, id }
  } = props;
  const url = `${constants.BASE_SOURCE}${id}`;

  return (
    <div className="main-player row">
      <Iframe title={title} src={url} />
      <div className="card col-sm-3 player-detail">
        <div className="card-body">
          <CardTitle title={title} />
          <CardDescription description={description} />
        </div>
      </div>
    </div>
  );
};

export default Player;
