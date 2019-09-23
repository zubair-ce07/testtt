import React from "react";
import { Card, ListItem, Label } from "../../components";
import "./ListView.css";

const ListView = props => (
  <div className="list-view">
    {props.moves.length ? (
      <Card>
        <Label text="Moves:" />
        <ul className="list-group">
          {props.moves.map(move => {
            return <ListItem item={move} />;
          })}
        </ul>
      </Card>
    ) : null}
  </div>
);

export { ListView };
