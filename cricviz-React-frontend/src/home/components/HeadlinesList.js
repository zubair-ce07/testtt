import React, {Component} from 'react';
import {Row, Col, Grid, Thumbnail, Button, ListGroup, ListGroupItem} from 'react-bootstrap';

class HeadlinesList extends Component {
  render(){
    return (
      <div>
        <ListGroup className="col-sm-4 list-group">
           <ListGroupItem href="#link1">
            <a href="#link1">{`Would have liked to take Kohli's wicket - Hasan Ali`}</a>
           </ListGroupItem>
           <ListGroupItem href="#link2">
            <a href="#link2">{`Murtagh, Balbirnie help Ireland draw level`}</a>
           </ListGroupItem>
           <ListGroupItem href="#link3">
            <a href="#link3">{`There will never be another Alastair Cook - Root`}</a>
           </ListGroupItem>
         </ListGroup>
      </div>
    );
  }
}

export default HeadlinesList;
