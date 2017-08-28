import * as React from "react";
import TodoAdd from "./TodoAdd";
import FilterLinks from "./FilterLinks";


const Header = () => (
    <div className="header">
        <TodoAdd/>
        <FilterLinks/>
    </div>
);

export default Header;
