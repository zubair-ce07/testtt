import React from "react";
import "./ListItem.css";

const ListItem = props => {
  return (
    <div className="list-item">
      <li className="list-group-item">
        {`Damge Recieved: ${props.item.userDamage}`}
      </li>
      <li className="list-group-item">
        {props.item.opponentDamage
          ? `Damge Given: ${props.item.opponentDamage}`
          : `Healed: ${props.item.userHeal}`}
      </li>
    </div>
  );
};
export { ListItem };
