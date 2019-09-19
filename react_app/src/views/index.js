import React from "react";
import { GAME_STATUS } from "../utils/constants";
import { HealthStatus } from "../views/HealthStatus";
import {ListView} from "./ListView";
import {ButtonView} from "./ButtonView";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      userPercentage: 100,
      opponentPercentage: 100,
      status: GAME_STATUS.start,
      moves: []
    };

    this.health = 100;
    this.isWinner = false;
    this.handleAttack = this.handleAttack.bind(this);
    this.handleHeal = this.handleHeal.bind(this);
    this.handleGiveUp = this.handleGiveUp.bind(this);
    this.handleStartGame = this.handleStartGame.bind(this);
    this.handleRestart = this.handleRestart.bind(this);
    this.resetState = this.resetState.bind(this);
  }

  getRandomNumber() {
    return Math.floor(Math.random() * (10 - 1 + 1)) + 1;
  }

  handleAttack() {
    const userDamage = this.getRandomNumber();
    const opponentDamage = this.getRandomNumber();

    if (this.state.userPercentage - userDamage <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        userPercentage: 0
      });
      return;
    }

    if (this.state.opponentPercentage - opponentDamage <= 0) {
      this.setState({
        status: GAME_STATUS.end,
        opponentPercentage: 0
      });
      this.isWinner = true;
      return;
    }
    const moves = [{ opponentDamage, userDamage }, ...this.state.moves];
    this.setState(state => ({
      userPercentage: state.userPercentage - userDamage,
      opponentPercentage: state.opponentPercentage - opponentDamage,
      moves: moves
    }));
  }

  handleHeal() {
    let userHeal = this.getRandomNumber();
    const userDamage = this.getRandomNumber();

    if (this.state.userPercentage - userDamage < 0) {
      this.setState({ status: GAME_STATUS.end });
      return;
    }

    if (this.state.userPercentage + userHeal - userDamage > this.health) {
      userHeal -=
        this.state.userPercentage + userHeal - userDamage - this.health;
    }
    const moves = [{ userDamage, userHeal }, ...this.state.moves];
    this.setState(state => ({
      userPercentage: state.userPercentage + userHeal - userDamage,
      moves: moves
    }));
  }

  handleGiveUp() {
    this.setState({ status: GAME_STATUS.end });
    this.isWinner = false;
  }

  handleStartGame() {
    this.resetState();
    this.setState({ status: GAME_STATUS.playing });
  }

  handleRestart() {
    this.resetState();
    this.setState({ status: GAME_STATUS.start });
  }

  resetState() {
    this.isWinner = false;
    this.setState({
      userPercentage: this.health,
      opponentPercentage: this.health,
      moves: []
    });
  }

  render() {
    return (
      <div>
        <HealthStatus
          user={{
            content: "User",
            percentage: this.state.userPercentage
          }}
          opponent={{
            content: "Opponent",
            percentage: this.state.opponentPercentage
          }}
        />
        <ButtonView
        status={this.state.status}
        handleAttack={this.handleAttack}
        handleGiveUp={this.handleGiveUp}
        handleHeal={this.handleHeal}
        handleStartGame={this.handleStartGame}
        handleRestart={this.handleRestart}
        isWinner={this.isWinner}
        />
        
        <ListView moves={this.state.moves}/>
      </div>
    );
  }
}

export { App };
