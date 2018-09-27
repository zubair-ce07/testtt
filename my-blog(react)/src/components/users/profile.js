import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';

// import { Col, Badge } from 'reactstrap';

const Profile = () => (
  <Fragment>
    <h2>Profile</h2>
    <h4>First Last</h4>
    <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. <br /></p>
    <p><Link className='btn btn-secondary' to='/blogs/1' role='button'>View details »</Link></p>
  </Fragment>
);

export default Profile;
