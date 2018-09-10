import React, {Component} from 'react';

class LoginForm extends Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert(`User: ${this.state.value} logging in`);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          UserName:
          <input type="text" name="username" value={this.state.value} onChange={this.handleChange} />
        </label>
        <label>
          Password:
          <input type="password" name="password" />
        </label>
        <input type="submit" value="Login" />
      </form>
    );
  }
}

export default LoginForm;
