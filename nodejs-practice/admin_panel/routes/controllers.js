const passwordUtility = require("../helpers/passwordUtility.js");
const strategy = require("./passport");
const mongo = require("./connect.js")

var db;

mongo.connect((err) => {
	if (err) throw err
	db = mongo.db.db("users_test").collection("users_test");
})

exports.viewUsers = function (req, res) {
	db.find((err, records)=> {
		records.toArray((err, array) => {
			res.json(array)
		})
	})
}

exports.addUser = function (req, res) {
	let userDetails = req.query

	if(!userDetails.username || !userDetails.name || !userDetails.admin || !userDetails.password) {
		res.json({response: "username, name, password, admin all MUST be provided!"})
		return
	}
	var salt = passwordUtility.genRandomString(16);
	let passwordObject = passwordUtility.sha512(userDetails.password, salt)
	
	db.findOne({username: userDetails.username}, (err, result) => {
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
				db.insertOne({
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
		db.deleteOne({username: usernameToDelete});
		res.json({response: `User ${usernameToDelete} was successfully deleted!`});
	} catch(e) {
		console.log(e)
		res.json({response: `Failed to delete the user: ${usernameToDelete}`})
	}
}

exports.updateUser = function (req, res) {
	let usernameToUpdate = req.query.username

	if(!usernameToUpdate) {
		res.json({response: "Please specify a USERNAME to `UPDATE` from database"});
		return;
	}
	
	try {
		db.findOne({username: usernameToUpdate}, (err, result) => {
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
				db.updateOne({username: usernameToUpdate}, {$set: update})
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
