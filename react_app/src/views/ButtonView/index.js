import React from "react";
import { Button, Label, Card } from "../../components";
import { GAME_STATUS, GAME_ACTION } from "../../utils/constants";
import "./ButtonView.css";

const ButtonView = props => (
  <div className="button-view">
    {props.status === GAME_STATUS.playing ? (
      <Card>
        <Button onClick={() => props.handleAction(GAME_ACTION.attack)} text="Attack" />
        <Button onClick={() => props.handleAction(GAME_ACTION.heal)} text="Heal" />
        <Button onClick={props.handleGiveUp} text="Give Up" />
      </Card>
    ) : (
      <Card>
        <Button
          onClick={() => props.handleGame(GAME_ACTION.start)}
          text="Start Game"
        />
        {props.status === GAME_STATUS.end && (
          <React.Fragment>
            <Button
              onClick={() => props.handleGame(GAME_ACTION.continue)}
              text="Continue"
            />
            <Card>
              <Label
                text={props.opponentPercentage <= 0 ? "You Win!" : "You Lose!"}
              />
            </Card>
          </React.Fragment>
        )}
      </Card>
    )}
  </div>
);

export { ButtonView };
