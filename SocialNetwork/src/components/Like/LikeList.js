import React from 'react';
import '../StyleSheets/PostList.css'

const LikeList = ({likes}) => (
	(likes.length > 0)
	  ? <div style={{marginTop: "2%"}}>
			{
				likes.map( like => {
					return(
						<div className="commentwell" key={like.id}> 
							<p>
								{like.user}
							</p>
						</div>
					);
				})
			}
			</div>
		
	  : <div>No likes found</div>
		
);

export default LikeList;