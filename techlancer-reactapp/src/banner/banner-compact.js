import React from 'react';
import SearchBox from './search-box.jsx';

export default class BannerCompact extends React.Component {
	render() {
		return (
			<div className="banner_1">
				<div className="container">
					<div id="search_wrapper1">
					 <SearchBox />
					</div>
				</div>
			</div>
		);
	}
}
