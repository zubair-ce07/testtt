import React from "react";
import { Button, Label, Card } from "../../components";
import { GAME_STATUS, GAME_ACTION } from "../../utils/constants";
import "./ButtonView.css";

const ButtonView = props => {
  const { attack, heal, start, cont } = GAME_ACTION;
  const { handleGame, handleAction, handleGiveUp } = props;
  return (
    <div className="button-view">
      <Card>
        {props.status === GAME_STATUS.playing ? (
          <React.Fragment>
            <Button onClick={() => handleAction(attack)} text="Attack" />
            <Button onClick={() => handleAction(heal)} text="Heal" />
            <Button onClick={handleGiveUp} text="Give Up" />
          </React.Fragment>
        ) : (
          <React.Fragment>
            <Button onClick={() => handleGame(start)} text="Start Game" />
            {props.status === GAME_STATUS.end && (
              <React.Fragment>
                <Button onClick={() => handleGame(cont)} text="Continue" />
                <Card>
                  <Label
                    text={
                      props.opponentPercentage <= 0 ? "You Win!" : "You Lose!"
                    }
                  />
                </Card>
              </React.Fragment>
            )}
          </React.Fragment>
        )}
      </Card>
    </div>
  );
};

export { ButtonView };
