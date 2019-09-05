import React from "react";
import { compose } from "redux";
import { connect } from "react-redux";
import { withRouter } from "react-router";

const withAuthorization = (condition, redirectUrl) => Component => {
  class WithAuthorization extends React.Component {
    componentDidMount() {
      const { token, history } = this.props;
      console.log(condition(token), redirectUrl);
      if (!condition(token)) history.replace(redirectUrl);
    }

    render() {
      return <Component {...this.props} />;
    }
  }

  const mapStateToProps = state => ({
    token: state.auth.token
  });

  return compose(
    withRouter,
    connect(mapStateToProps)
  )(WithAuthorization);
};

export default withAuthorization;
