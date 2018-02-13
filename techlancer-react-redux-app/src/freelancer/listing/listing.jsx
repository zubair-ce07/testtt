import { bindActionCreators } from 'redux';
import * as Actions from './actions.js';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom'
import React from 'react';

import PropTypes from 'prop-types';

import BannerCompact from '../../banner/banner-compact';
import ListItem from './listItem';

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch)
  };
}
function mapStateToProps(state) {
  return {
    freelancers: state.freelancer_reducer.freelancers
  };
}

class Listing extends React.Component {
	componentWillMount() {
     this.props.actions.fetchFreelancers();
   }
	static propTypes = {
	    freelancers: PropTypes.array,
	};

	renderList(){
			let freelancers = []
			for (let freelancer of this.props.freelancers) {
 		  	 	freelancers.push(<ListItem username={freelancer.username}/>)
			}
			return freelancers;
    }

	render() {
		return (
			<div>
				<BannerCompact/>    
				<div className="container">
				    <div className="single">  
				      <div className="col-sm-10 follow_left">
							<h3>Freelancers</h3>
				             <div className="follow_jobs">
								{this.renderList()}
								<ul className="pagination hidden">
									<li className="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true">«</span></a></li>
									<li className="active"><a href="#">1 <span className="sr-only">(current)</span></a></li>
									<li><a href="#">2</a></li>
									<li><a href="#">3</a></li>
									<li><a href="#">4</a></li>
									<li><a href="#">5</a></li>
									<li><a href="#" aria-label="Next"><span aria-hidden="true">»</span></a></li>
							   </ul>
						    </div>
						</div>
						<div className="clearfix"> </div>
					</div>
				</div>
			</div> )
	}
}

export default withRouter(connect(
    mapStateToProps,
    mapDispatchToProps
)(Listing));
