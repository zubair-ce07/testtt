import React from "react";
import {
  DEFAULT_HEALTH,
  GAME_ACTION,
  GAME_STATUS,
  getRandomNumber
} from "../utils/constants";
import { HealthStatus } from "../views/HealthStatus";
import { ListView } from "./ListView";
import { ButtonView } from "./ButtonView";

class App extends React.Component {
  state = {
    userPercentage: DEFAULT_HEALTH,
    opponentPercentage: DEFAULT_HEALTH,
    status: GAME_STATUS.start,
    moves: []
  };

  handleAction = action => {
    const userDamage = getRandomNumber();
    let userAction = getRandomNumber();

    if (this.state.userPercentage - userDamage <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        userPercentage: 0
      });
      return;
    }

    if (action === GAME_ACTION.heal) {
      if (
        this.state.userPercentage + userAction - userDamage >
        DEFAULT_HEALTH
      ) {
        userAction -=
          this.state.userPercentage + userAction - userDamage - DEFAULT_HEALTH;
      }

      const moves = [{ userDamage, userHeal: userAction }, ...this.state.moves];
      this.setState(state => ({
        userPercentage: state.userPercentage + userAction - userDamage,
        moves
      }));
      return;
    }

    if (this.state.opponentPercentage - userAction <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        opponentPercentage: 0
      });
      this.isWinner = true;
      return;
    }

    const moves = [
      { opponentDamage: userAction, userDamage },
      ...this.state.moves
    ];
    this.setState({
      opponentPercentage: this.state.opponentPercentage - userAction,
      userPercentage: this.state.userPercentage - userDamage,
      moves
    });
  };

  handleGame = action => {
    const status =
      action === GAME_ACTION.start ? GAME_STATUS.playing : GAME_STATUS.start;
    this.setState({
      userPercentage: DEFAULT_HEALTH,
      opponentPercentage: DEFAULT_HEALTH,
      moves: [],
      status
    });
  };

  render() {
    const healthStatus = {
      user: {
        content: "User",
        percentage: this.state.userPercentage
      },
      opponent: {
        content: "Opponent",
        percentage: this.state.opponentPercentage
      }
    };
    return (
      <React.Fragment>
        <HealthStatus data={healthStatus} />
        <ButtonView
          status={this.state.status}
          opponentPercentage={this.state.opponentPercentage}
          handleAction={this.handleAction}
          handleGame={this.handleGame}
          handleGiveUp={() => this.setState({ status: GAME_STATUS.end })}
        />
        <ListView moves={this.state.moves} />
      </React.Fragment>
    );
  }
}

export { App };
