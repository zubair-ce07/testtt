import React from 'react';

const Iframe = ({ title, src }) => {
  return <iframe className="col-sm-9" title={title} src={src} />;
};

export default Iframe;
