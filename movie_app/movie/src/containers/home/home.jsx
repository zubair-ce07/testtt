import React from "react";
import { Button } from "../../components";

class Home extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-4 offset-sm-4">
            <h3>
              {`Welcome ${this.props.user.first_name} ${this.props.user.last_name}`}
            </h3>
            <Button
              text="Logout"
              className="btn-primary btn-block"
              type="button"
              onClick={this.props.logoutUser}
            />
          </div>
        </div>
      </div>
    );
  }
}

export { Home };
