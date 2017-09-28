import React from 'react';
import '../StyleSheets/PostList.css'

const LikeList = ({likes}) => {
		if(likes.length > 0)
		{
			return (
				<div style={{marginTop: "2%"}}>
					{
						likes.map( like => {
							return(
							<div className="commentwell" key={like.id}> 
								<p>{like.user}</p>
							</div>
							);

						})
					}
				</div>
			);
		}
		else{
			return <div>No likes found</div>
		}
}

export default LikeList;