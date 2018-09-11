import React, {Component} from 'react';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import FollowTeamsListItem from './FollowTeamsListItem';

const FollowTeamsList = (props) => {
  const AllTeams = props.teams.map((team) => {
    return (
      <FollowTeamsListItem
        key={team.url}
        team={team} />
      );
    });

  return (
    <ul className=" col-md-6 list-group">
      {AllTeams}
    </ul>
  );
}

export default FollowTeamsList;
