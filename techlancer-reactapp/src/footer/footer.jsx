import React from 'react';

export default class Footer extends React.Component {
	render() {
		return (
				<div>
					<div class="footer">
						<div class="container">
							<div class="col-md-3 grid_3">
								<h4>Navigate</h4>
								<ul class="f_list f_list1">
									<li><a href="index.html">Home</a></li>
									<li><a href="login.html">Sign In</a></li>
									<li><a href="login.html">Join Now</a></li>
									<li><a href="about.html">About</a></li>
								</ul>
								<ul class="f_list">
									<li><a href="features.html">Features</a></li>
									<li><a href="terms.html">Terms of use</a></li>
									<li><a href="contact.html">Contact Us</a></li>
									<li><a href="jobs.html">Post a Job</a></li>
								</ul>
								<div class="clearfix"> </div>
							</div>
							<div class="col-md-3 grid_3">
								<h4>Twitter Widget</h4>
								<div class="footer-list">
								  <ul>
									<li><i class="fa fa-twitter tw1"> </i><p><span class="yellow"><a href="#">consectetuer</a></span> adipiscing elit web design</p></li>
									<li><i class="fa fa-twitter tw1"> </i><p><span class="yellow"><a href="#">consectetuer</a></span> adipiscing elit web design</p></li>
									<li><i class="fa fa-twitter tw1"> </i><p><span class="yellow"><a href="#">consectetuer</a></span> adipiscing elit web design</p></li>
								  </ul>
								</div>
							</div>
							<div class="col-md-3 grid_3">
								<h4>Seeking</h4>
								<p>There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. </p>
							</div>
							<div class="col-md-3 grid_3">
								<h4>Sign up for our newsletter</h4>
								<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam.</p>
								<form>
									<input type="text" class="form-control" placeholder="Enter your email"/>
									<button type="button" class="btn red">Subscribe now!</button>
							    </form>
							</div>
							<div class="clearfix"> </div>
						</div>
					</div>
					<div class="footer_bottom">	
					  <div class="container">
					    <div class="col-sm-2">
					  		<ul class="f_list2">
								<li><a href="jobs.html">Russia Jobs</a></li>
								<li><a href="jobs.html">Australia Jobs</a></li>
								<li><a href="jobs.html">Srilanka Jobs</a></li>
								<li><a href="jobs.html">Poland Jobs</a></li>
						    </ul>
					  	</div>
					  	<div class="col-sm-2">
					  		<ul class="f_list2">
								<li><a href="jobs.html">New Zealand Jobs</a></li>
								<li><a href="jobs.html">Pakistan Jobs</a></li>
								<li><a href="jobs.html">Srilanka Jobs</a></li>
								<li><a href="jobs.html">Irland Jobs</a></li>
						    </ul>
					  	</div>
					  	<div class="col-sm-2">
					  		<ul class="f_list2">
								<li><a href="jobs.html">Canada Jobs</a></li>
								<li><a href="jobs.html">Germany Jobs</a></li>
								<li><a href="jobs.html">China Jobs</a></li>
								<li><a href="jobs.html">Nepal Jobs</a></li>
						    </ul>
					  	</div>
					  	<div class="col-sm-6 footer_text">
					       <p>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numqua"</p>
					  	</div>
					  	<div class="clearfix"> </div>
						<div class="copy">
							<p>Copyright © 2015 Seeking . All Rights Reserved . Design by <a href="http://w3layouts.com/" target="_blank">W3layouts</a> </p>
						</div>
					  </div>
					</div>
				</div>
		);
	}
}
