import React from "react";
import { BrowserRouter as Router, Link } from "react-router-dom";
import { mainStyle } from "./styles";
import { routes } from "../routes";

const Landing = () => {
  return (
    <div style={mainStyle} className="jumbotron text-center">
      <h1 className="display-4">Instructions</h1>
      <p className="lead font-weight-bold">Think of a 2 digit number</p>
      <p className="lead">i-e 32</p>
      <p className="lead font-weight-bold">Add both the digits</p>
      <p className="lead ">3 + 2 = 5</p>
      <p className="lead font-weight-bold">
        Subtract the sum from the actual number
      </p>
      <p className="lead ">32 - 5 = 27</p>
      <hr />
      <p className="lead font-weight-bold">
        On next page, you will see random images,
      </p>
      <p className="lead font-weight-bold">
        remeber the image against the finnal result
      </p>
      <p className="lead">
        <Link className="btn btn-primary btn-lg" to={routes.iconsList.path}>
          Get Started
        </Link>
      </p>
    </div>
  );
};

export default Landing;
