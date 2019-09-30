import React from "react";

class Home extends React.Component {
  render() {
    return (
      <h1>
        Welcome {`${this.props.user.first_name} ${this.props.user.last_name}`}
      </h1>
    );
  }
}

export { Home };
