import React from "react";
import { GAME_STATUS, GAME_ACTION } from "../utils/constants";
import { HealthStatus } from "../views/HealthStatus";
import { ListView } from "./ListView";
import { ButtonView } from "./ButtonView";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userPercentage: 100,
      opponentPercentage: 100,
      status: GAME_STATUS.start,
      moves: []
    };
  }

  getRandomNumber = () => {
    return Math.floor(Math.random() * (10 - 1 + 1)) + 1;
  };

  handleAction = action => {
    const userDamage = this.getRandomNumber();
    let heal = this.getRandomNumber();

    if (this.state.userPercentage - userDamage <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        userPercentage: 0
      });
      return;
    }

    if (action === "Heal") {
      if (this.state.userPercentage + heal - userDamage > 100) {
        heal -= this.state.userPercentage + heal - userDamage - 100;
      }

      const moves = [{ userDamage, userHeal: heal }, ...this.state.moves];
      this.setState(state => ({
        userPercentage: state.userPercentage + heal - userDamage,
        moves
      }));
      return;
    }

    if (this.state.opponentPercentage - heal <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        opponentPercentage: 0
      });
      this.isWinner = true;
      return;
    }

    const moves = [{ opponentDamage: heal, userDamage }, ...this.state.moves];
    this.setState({
      opponentPercentage: this.state.opponentPercentage - heal,
      userPercentage: this.state.userPercentage - userDamage,
      moves
    });
  };

  handleGame = action => {
    const status =
      action === GAME_ACTION.start ? GAME_STATUS.playing : GAME_STATUS.start;
    this.setState({
      userPercentage: this.health,
      opponentPercentage: this.health,
      moves: [],
      status
    });
  };

  render() {
    return (
      <React.Fragment>
        <HealthStatus
          data={{
            user: {
              content: "User",
              percentage: this.state.userPercentage
            },
            opponent: {
              content: "Opponent",
              percentage: this.state.opponentPercentage
            }
          }}
        />
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
