let months = [
    'January', 'February', 'March', 'April', 'May',
    'June', 'July', 'August', 'September',
    'October', 'November', 'December'
    ];


function logout()
{
   sessionStorage.removeItem("loggedin_user");
   window.location.href = "login.html";
}


function get_current_date()
{
	let date = new Date();
	month = months[date.getMonth()-1]
    return `${month} ${date.getDate()}, ${date.getFullYear()}`;
}


function increase_comment_badge(post_id)
{
	let comment_badge = document.getElementById(`${post_id}_comment_badge`)
	count = comment_badge.innerHTML
	count= parseInt(count, 10)+1
	comment_badge.innerHTML = count
}


function get_post_div()
{
	let post_template = document.getElementsByName("post_template")[0]
	var post_div = post_template.cloneNode(true)
			
	post_div.style.display = "block"
    post_div.removeAttribute("name")
    return post_div
}


function display_comment(comment_container, comment)
{
	comment_div = comment_container.firstElementChild.cloneNode(true)
	comment_div.getElementsByClassName("comment_by")[0].innerHTML = comment["comment_by"]
	comment_div.getElementsByClassName("comment")[0].innerHTML = comment["comment"]
	comment_container.appendChild(comment_div)
}

function display_post(user_post, post_div)
{
	let logged_in_user = JSON.parse(sessionStorage.getItem("loggedin_user"));
	if(!(user_post["likes[]"]))
		user_post["likes[]"] =  new Array()
    else if (!Array.isArray(user_post["likes[]"]))
    {	
    	let arr = new Array()
        arr.push(user_post["likes[]"])
        user_post["likes[]"] = arr
    }  

    post_div.getElementsByClassName("post_username")[0].innerHTML = user_post["post_user"]["username"]
	post_div.getElementsByClassName("post_date")[0].innerHTML = user_post.date
	post_div.getElementsByClassName("post_title")[0].innerHTML = user_post.title
	post_div.getElementsByClassName("post_data")[0].innerHTML = user_post.post
	
	let comment_badge = post_div.getElementsByClassName("post_comment_count")[0]
	comment_badge.innerHTML =  user_post["post_comments"].length
	comment_badge.id = `${user_post.id}_comment_badge`

	let like_badge = post_div.getElementsByClassName("post_likes")[0]
	like_badge.innerHTML = user_post["likes[]"].length
	like_badge.id = `${user_post.id}_likecount`
    
    let like_element = post_div.getElementsByClassName("like")[0]
    like_element.id =  `${user_post.id}_like`

    if(user_post["likes[]"].includes(logged_in_user.username))
        like_element.classList.add("fa-thumbs-down");
    else
        like_element.classList.add("fa-thumbs-up");

    post_div.getElementsByClassName("comment_btn")[0].id =  `${user_post.id}_btn`
    post_div.getElementsByClassName("comment_area")[0].id =  `${user_post.id}_comment`

    let comment_container = post_div.getElementsByClassName("comment_container")[0]
    comment_container.id = `${user_post.id}_comments`

    for(let comment of user_post["post_comments"])
    	display_comment(comment_container, comment)
}


function make_post()
{
	let logged_in_user = JSON.parse(sessionStorage.getItem("loggedin_user"));
	if(logged_in_user)
	{
		let formData = {
			"title": document.getElementById("new_post_title").value,
			"post": document.getElementById("new_post_text").value,
			"date": get_current_date()			
		};

		$.ajax({
			type        : 'POST',
			url         : `http://localhost:3000/users/${logged_in_user.id}/posts`, 
			data        : formData, 
			dataType    : 'json' 
		})
		.done(new_post => 
		{
			let post_container = document.getElementById("post_container")
			post_div = get_post_div()
			new_post["post_comments"] = []
			new_post["post_user"] = logged_in_user
			display_post(new_post, post_div)
    	    post_container.appendChild(post_div)
		})
	}
}


function make_comment(btn)
{
	let post_id = (btn.id.split("_"))[0];
	let logged_in_user = JSON.parse(sessionStorage.getItem("loggedin_user"));
	
	let formData = {
		"comment_by": logged_in_user.username,
		"comment": document.getElementById(`${post_id}_comment`).value 
	};

	$.ajax({
		type        : 'POST',
		url         : `http://localhost:3000/posts/${post_id}/comments`, 
		data        : formData, 
		dataType    : 'json' 
	})
	.done(comment =>
	{
		let comment_container = document.getElementById(`${comment.postId}_comments`)
		display_comment(comment_container, comment)
		increase_comment_badge(comment.postId)
	})
}


function make_like(btn)
{
	let logged_in_user = JSON.parse(sessionStorage.getItem("loggedin_user"));
	btn.classList.toggle("fa-thumbs-down");
	let post_id = (btn.id.split("_"))[0];

	fetch(`http://localhost:3000/posts/${post_id}`)
	.then(response => response.json())
    .then(post => 
    {
    	if(!(post["likes[]"]))
        	post["likes[]"] =  new Array()
        else if (!Array.isArray(post["likes[]"]))
        {	
        	let arr = new Array()
        	arr.push(post["likes[]"])
        	post["likes[]"] = arr
        }
 
    	like_index = post["likes[]"].findIndex(username => username == logged_in_user.username)
        if(like_index!=-1)
            post["likes[]"].splice(like_index, 1);
        else
            post["likes[]"].push(logged_in_user.username)
    	
    	$.ajax({
    		type        : 'PUT',
    		url         : `http://localhost:3000/posts/${post_id}`, 
    		data        : post,
    		dataType    : 'json' 
    	})
    	.done(data => document.getElementById(`${post_id}_likecount`).innerHTML = post["likes[]"].length )
    })
    .catch(alert);
}


let logged_in_user = JSON.parse(sessionStorage.getItem("loggedin_user"));
fetch(`http://localhost:3000/posts`)
.then(response => response.json())
.then(post_list => 
{
	let post_container = document.getElementById("post_container")
    for (let user_post of post_list) 
    {
    	fetch(`http://localhost:3000/posts/${user_post.id}/comments`)
    	.then(response => response.json())
    	.then(post_comments => 
    	{
    		user_post["post_comments"] = post_comments
    		if(logged_in_user.id == user_post.userId)
    			user_post["post_user"] = logged_in_user
    		else
    		{
    			fetch(`http://localhost:3000/users/${user_post.userId}`)
    			.then(response => response.json())
    			.then(post_user => 
    			{
    				user_post["post_user"] = post_user
    	    	})
    	    	.catch(alert);
    		}
    		post_div = get_post_div()
    		display_post(user_post, post_div)
    	    post_container.appendChild(post_div)
    	}).catch(alert);
	}
}).catch(alert);