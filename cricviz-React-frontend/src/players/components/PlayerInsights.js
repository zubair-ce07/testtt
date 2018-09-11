import React, {Component} from 'react';
import {FormGroup, ControlLabel, FormControl, Button} from 'react-bootstrap';
import PlayerInsightsList from './PlayerInsightsList';
import PLAYERS from '../PlayersData';

class PlayerInsights extends Component {
  constructor(props) {
    super(props);
    this.state = {players: PLAYERS};

  }
  render() {
    return (
      <div>
        <h1>Players Insights</h1>
        <br></br>
        <div className="col-md-2">
          <form>

            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Format</ControlLabel>
              <FormControl componentClass="select" placeholder="select">
                <option value="All">All</option>
                <option value="Tests">Tests</option>
                <option value="ODIs">ODIs</option>
                <option value="T20Is">T20Is</option>
                <option value="FirstClass">FirstClass</option>
                <option value="List A">List A</option>
                <option value="T20s">T20s</option>
              </FormControl>
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Playing Role</ControlLabel>
              <FormControl componentClass="select" placeholder="select">
                <option value="All">All</option>
                <option value="Batsman">Batsman</option>
                <option value="Bowler">Bowler</option>
                <option value="AllRounder">AllRounder</option>
                <option value="WicketKeeper">WicketKeeper</option>
              </FormControl>
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Minimum Matches</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Minimum Innings</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Runs Scored</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
              <FormControl componentClass="textarea" placeholder="max" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Batting Average</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Hundreds</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Fifties</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Fours</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Sixes</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Catches</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
            </FormGroup>
            <FormGroup controlId="formControlsSelect">
              <ControlLabel>Wickets Taken</ControlLabel>
              <FormControl componentClass="textarea" placeholder="min" />
              <FormControl componentClass="textarea" placeholder="max" />
            </FormGroup>


            <Button type="submit">Submit</Button>

          </form>
        </div>

        <PlayerInsightsList players={this.state.players} />

      </div>

    );
  }
}

export default PlayerInsights;
