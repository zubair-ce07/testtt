import React from 'react';
import { string, shape } from 'prop-types';

import * as constants from '../../shared/constants';
import CardTitle from './cardTitle';
import CardDescription from './cardDescription';
import Iframe from './iframe';

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

Player.propTypes = {
  source: shape({
    title: string,
    description: string,
    id: string,
    thumbnail: string
  })
};

export default Player;
