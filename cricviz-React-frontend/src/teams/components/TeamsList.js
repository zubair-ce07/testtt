import React, {Component} from 'react';
import {ListGroup, ListGroupItem} from 'react-bootstrap';
import TeamsListItem from './TeamsListItem';

const TeamsList = (props) => {
  const AllTeams = props.teams.map((team) => {
    return (
      <TeamsListItem
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

export default TeamsList;
