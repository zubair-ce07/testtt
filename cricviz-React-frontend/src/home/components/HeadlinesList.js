import React, {Component} from 'react';
import {ListGroup, ListGroupItem} from 'react-bootstrap';

class HeadlinesList extends Component {
  render(){
    return (
      <div>
        <article className="col-sm-4">
          <h3 className="text-left">Top Headlines</h3>
        </article>

        <ListGroup className="col-sm-4 list-group">
           <ListGroupItem>
            <a href="#link1">{`Would have liked to take Kohli's wicket - Hasan Ali`}</a>
           </ListGroupItem>
           <ListGroupItem>
            <a href="#link2">{`Murtagh, Balbirnie help Ireland draw level`}</a>
           </ListGroupItem>
           <ListGroupItem>
            <a href="#link3">{`There will never be another Alastair Cook - Root`}</a>
           </ListGroupItem>
         </ListGroup>
      </div>
    );
  }
}

export default HeadlinesList;
