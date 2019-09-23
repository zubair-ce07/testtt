import React from "react";
import "./ListItem.css";

const ListItem = props => (
  <div className="list-item">
    <li className="list-group-item">
      {`Damage Recieved: ${props.item.userDamage}`}
    </li>
    <li className="list-group-item">
      {props.item.opponentDamage
        ? `Damage Given: ${props.item.opponentDamage}`
        : `Healed: ${props.item.userHeal}`}
    </li>
  </div>
);

export { ListItem };
