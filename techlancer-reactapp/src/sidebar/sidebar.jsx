import React from 'react';

export default class Sidebar extends React.Component {
	render() {
		return (
			 <div className="col-md-4">
			   	  <div className="col_3">
			   	  	<h3>Todays Jobs</h3>
			   	  	<ul className="list_1">
			   	  		<li><a href="#">Department of Health - Western Australia</a></li>
			   	  		<li><a href="#">Australian Nursing Agency currently require experiences</a></li>		
			   	  		<li><a href="#">Russia Nursing Agency currently require experiences</a></li>
			   	  		<li><a href="#">The Government of Western Saudi Arbia</a></li>		
			   	  		<li><a href="#">Department of Health - Western Australia</a></li>
			   	  		<li><a href="#">Australian Nursing Agency currently require experiences</a></li>		
			   	  		<li><a href="#">Russia Nursing Agency currently require experiences</a></li>
			   	  		<li><a href="#">The Scientific Publishing Services in Saudi Arbia</a></li>	
			   	  		<li><a href="#">BPO Private Limited in Canada</a></li>		
			   	  		<li><a href="#">Executive Tracks Associates in Pakistan</a></li>
			   	  		<li><a href="#">Pyramid IT Consulting Pvt. Ltd. in Pakistan</a></li>						
			   	  	</ul>
			   	  </div>
			   	  <div className="col_3">
			   	  	<h3>Jobs by Category</h3>
			   	  	<ul className="list_2">
			   	  		<li><a href="#">Railway Recruitment</a></li>
			   	  		<li><a href="#">Air Force Jobs</a></li>		
			   	  		<li><a href="#">Police Jobs</a></li>
			   	  		<li><a href="#">Intelligence Bureau Jobs</a></li>		
			   	  		<li><a href="#">Army Jobs</a></li>
			   	  		<li><a href="#">Navy Jobs</a></li>		
			   	  		<li><a href="#">BSNL Jobs</a></li>
			   	  		<li><a href="#">Software Jobs</a></li>	
			   	  		<li><a href="#">Research Jobs</a></li>								
			   	  	</ul>
			   	  </div>
			   	  <div className="widget">
			        <h3>Take The Seeking Poll!</h3>
		    	        <div className="widget-content"> 
		                 <div className="seeking-answer">
					    	<span className="seeking-answer-group">
				    			<span className="seeking-answer-input">
				    			   <input className="seeking-radiobutton" type="radio"/>
				    			</span>
				    			<label htmlFor="" className="seeking-input-label">
				    				<span className="seeking-answer-span">Frequently</span>
				    			</label>
				    		</span>
					    	<span className="seeking-answer-group">
				    			<span className="seeking-answer-input">
				    			   <input className="seeking-radiobutton" type="radio"/>
				    			</span>
				    			<label htmlFor="" className="seeking-input-label">
				    				<span className="seeking-answer-span">Interviewing</span>
				    			</label>
				    		</span>
					        <span className="seeking-answer-group">
				    			<span className="seeking-answer-input">
				    			   <input className="seeking-radiobutton" type="radio"/>
				    			</span>
				    			<label htmlFor="" className="seeking-input-label">
				    				<span className="seeking-answer-span">Leaving a familiar workplace</span>
				    			</label>
				    		</span>
				    		<div className="seeking_vote">
				    		  <a className="seeking-vote-button">Vote</a>
				    		</div>
					     </div>
		    	       </div>
		    	</div>
			 </div>
		);
	}
}
