import React, { Fragment } from 'react';
import { Badge } from 'reactstrap';

const Tag = ({ name }) => (
  <Fragment>
    <Badge color="primary">{name}</Badge>&nbsp;
  </Fragment>
);

export default Tag;
