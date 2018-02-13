import React from 'react';

export default class SearchBox extends React.Component {
	render() {
		return (
				<div id="search_form" className="clearfix">
					<h1>Start your job search</h1>
					    <p>
						 <input type="text" className="text" placeholder=" 	"/>
						 <input type="text" className="text" placeholder=" "/>
						 <label className="btn2 btn-2 btn2-1b"><input type="submit" value="Find Jobs"/></label>
						</p>
			        <h2 className="title">top Countries &amp; searches</h2>
			    </div>
		);
	}
}
