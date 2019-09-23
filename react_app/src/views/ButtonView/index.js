import React from "react";
import { Button, Label, Card } from "../../components";
import { GAME_STATUS, GAME_ACTION } from "../../utils/constants";
import "./ButtonView.css";

const ButtonView = ({
  handleGame,
  handleAction,
  handleGiveUp,
  opponentPercentage,
  status
}) => {
  const { attack, heal, start, cont } = GAME_ACTION;
  return (
    <div className="button-view">
      <Card>
        {status === GAME_STATUS.playing ? (
          <React.Fragment>
            <Button onClick={() => handleAction(attack)} text="Attack" />
            <Button onClick={() => handleAction(heal)} text="Heal" />
            <Button onClick={handleGiveUp} text="Give Up" />
          </React.Fragment>
        ) : (
          <React.Fragment>
            <Button onClick={() => handleGame(start)} text="Start Game" />
            {status === GAME_STATUS.end && (
              <React.Fragment>
                <Button onClick={() => handleGame(cont)} text="Continue" />
                <Card>
                  <Label
                    text={opponentPercentage <= 0 ? "You Win!" : "You Lose!"}
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
