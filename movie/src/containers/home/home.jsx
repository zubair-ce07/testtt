import React from "react";
import { Button } from "../../components";
import "./home.css";

class Home extends React.Component {
  handleLogout = () => this.props.logoutUser();
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-4 home">
            <h3>
              Welcome{" "}
              {`${this.props.user.first_name} ${this.props.user.last_name}`}
            </h3>
            <Button
              text="Logout"
              type="btn-primary"
              onClick={this.handleLogout}
            />
          </div>
        </div>
      </div>
    );
  }
}

export { Home };
