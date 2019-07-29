const passwordUtility = require("../helpers/passwordUtility.js");
const strategy = require("./passport");
const mongo = require("./connect.js")

var collection;

mongo.connect((err) => {
	if (err) throw err
	collection = mongo.database.collection("users_test");
})


exports.showProfile = function (req, res) {
	let user = req.user;
		res.json({userDetails: {
			id: user.id,
			username: user.username,
			name: user.name,
			admin: user.admin
		}
	})
}

exports.viewUsers = function (req, res) {
	collection.find({},
					{projection:{_id: 0, password_salt: 0, password_hash: 0}},
					(err, records)=> {
						if (err) throw err;
						records.toArray((err, array) => {
							if (err) throw err;
							console.log(array)
							res.json(array)
						})
					})
}

exports.addUser = function (req, res) {
	let userDetails = req.query

	if(!userDetails.username || !userDetails.name || !userDetails.admin || !userDetails.password) {
		res.json({response: "`username`, `name`, `password`, `admin` all MUST be provided!"})
		return
	}
	var salt = passwordUtility.genRandomString(16);
	let passwordObject = passwordUtility.sha512(userDetails.password, salt)
	
	collection.findOne({username: userDetails.username}, (err, result) => {
		if (err) {
			console.log(err);
			res.json({response: "Sorry, there was an error..."})
			return err;
		}
		
		if(result) {
			res.json({response: `Sorry, user with ${userDetails.username} already exists...`})
			return;
		} else {
			try {
				collection.insertOne({
					username: userDetails.username, 
					name: userDetails.name, 
					admin: userDetails.admin, 
					password_hash: passwordObject.passwordHash, 
					password_salt: passwordObject.salt})
				res.json({response: `User ${userDetails.username} was successfully added!`});
			} catch (e) {
				res.json({response: "Sorry, there was an error..."})
				return err
			}
		}
	})
}


exports.deleteUser = function (req, res) {
	let usernameToDelete = req.query.username

	if(!usernameToDelete) {
		res.json({response: "Please specify a USERNAME to delete from database"});
		return;
	}
	
	try {
		collection.deleteOne({username: usernameToDelete});
		res.json({response: `User ${usernameToDelete} was successfully deleted!`});
	} catch(e) {
		console.log(e)
		res.json({response: `Failed to delete the user: ${usernameToDelete}`})
	}
}


exports.updateUser = function (req, res) {
	let userDetails = req.query
	let usernameToUpdate = userDetails.username

	if (req.method == "PUT") {
		if (!userDetails.username || !userDetails.name || 
			!userDetails.admin || !userDetails.password) {
				res.json({response: "When using PUT: `username`, `name`, `password`, `admin` all MUST be provided!"})
				return
			}
			
	}

	if(!usernameToUpdate) {
		res.json({response: "Please specify a USERNAME to `UPDATE` from database"});
		return;
	}
	
	try {
		collection.findOne({username: usernameToUpdate}, (err, result) => {
			if (err) throw err;
			if(result) {
				let update = {}
				for(key in result) {
					if(key == "password") {
						continue;
					}
					if(key in req.query) {
						update[key] = req.query[key]
					} else {
						update[key] = result[key]
					}
				}
				if("password" in req.query) {
					const salt = passwordUtility.genRandomString(16);
					let passwordObject = passwordUtility.sha512(req.query["password"], salt)
					update["password_hash"] = passwordObject.passwordHash
					update["password_salt"] = passwordObject.salt
				}
				collection.updateOne({username: usernameToUpdate}, {$set: update})
				res.send({response: "Update applied"})
			} else {
				res.json({response: `No user with username ${usernameToUpdate} exists in the database`});
				return;
			}
		});
	} catch(e) {
		console.log(e)
		res.json({response: `Failed to update the user: ${usernameToUpdate}`})
	}
}
