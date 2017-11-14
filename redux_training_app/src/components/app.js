import React from 'react';
import ReduxToastr from 'react-redux-toastr';

export default class App extends React.Component {
  render() {
    return (
      <div>
        { this.props.children }
        <ReduxToastr
          timeOut={ 2000 }
          newestOnTop={ true }
          preventDuplicates
          position="top-right"
          transitionOut="fadeOut"
          progressBar={ false }/>
        </div>
    );
  }
}
