import React from "react";
import { Button, Label, Card } from "../../components";
import { GAME_STATUS } from "../../utils/constants";
import "./ButtonView.css";

const ButtonView = props => {
  return (
    <div className="button-view">
      {props.status === GAME_STATUS.playing ? (
        <Card>
          <Button action={props.handleAttack} content="Attack" />
          <Button action={props.handleHeal} content="Heal" />
          <Button action={props.handleGiveUp} content="Give Up" />
        </Card>
      ) : null}
      {props.status === GAME_STATUS.end ? (
        <Card>
          <Label content={props.isWinner ? "You Win!" : "You Lose!"} />
          <Card>
            <Button action={props.handleRestart} content="Start Game" />
            <Button action={props.handleStartGame} content="Continue" />
          </Card>
        </Card>
      ) : props.status === GAME_STATUS.start ? (
        <Card>
          <Button action={props.handleStartGame} content="Start Game" />
        </Card>
      ) : null}
    </div>
  );
};

export { ButtonView };
