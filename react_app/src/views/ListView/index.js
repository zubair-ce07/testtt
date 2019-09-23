import React from "react";
import { Card, ListItem, Label } from "../../components";
import "./ListView.css";

const ListView = ({ moves }) => (
  <div className="list-view">
    {moves.length ? (
      <Card>
        <Label text="Moves:" />
        <ul className="list-group">
          {moves.map(move => {
            return <ListItem item={move} />;
          })}
        </ul>
      </Card>
    ) : null}
  </div>
);

export { ListView };
