import React from 'react';
import BannerCompact from '../../banner/banner-compact';
import Freelancer from '../../models/Freelancer';
import ListItem from './listItem';

export default class Listing extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			freelancers:[]
		}
		this.renderList();
	}

	renderList(){
		var freelancer = new Freelancer();
		freelancer.getAll().then((freelancersJSON) => {
			let freelancers = []
			for (let freelancer of freelancersJSON) {
 		  	 	freelancers.push(<ListItem username={freelancer.username}/>)
			}
			this.setState({
				freelancers:freelancers
			});
		});
       
             
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
								{this.state.freelancers}
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
