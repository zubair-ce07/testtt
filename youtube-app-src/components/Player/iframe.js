import React from 'react';
import { string } from 'prop-types';

const Iframe = ({ title, source }) => {
  return <iframe className="col-sm-9" title={title} src={source} />;
};

Iframe.propTypes = {
  title: string,
  src: string
};

export default Iframe;
