import React from 'react';
import Sidebar from '../sidebar/sidebar.jsx';
import Banner from '../banner/banner.jsx'

export default class Home extends React.Component {
  render() {
    return (
      <div>
          <Banner/> 
           <div className="container"> 
          <Sidebar/>
        </div>
      </div>
    );
  }
}
