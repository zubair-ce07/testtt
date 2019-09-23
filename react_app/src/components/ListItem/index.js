import React from "react";
import "./ListItem.css";

const ListItem = ({ item: { userDamage, userHeal, opponentDamage } }) => (
  <div className="list-item">
    <li className="list-group-item">
      {`Damage Recieved: ${userDamage}  `}
      {opponentDamage
        ? `Damage Given: ${opponentDamage}`
        : `Healed: ${userHeal}`}
    </li>
  </div>
);

export { ListItem };
