const passwordUtility = require("../helpers/passwordUtility.js");
const strategy = require("../config/passport.js");
const promises = require("./DbPromises.js")


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
	promises.findAll()
	.then((records)=> {
		records.toArray((err, array) => {
			if (err) throw err;
			res.json(array)
		})
	})
	.catch((err) => {
		throw err
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
	
	promises.findOne(userDetails.username)
	.then((result) => {
		if(result) {
			res.json({response: `Sorry, user with ${userDetails.username} already exists...`})
			return;
		} else {

			promises.insertOne(userDetails, passwordObject)
			.then(() => {
				res.json({response: `User ${userDetails.username} was successfully added!`});
			})
			.catch((err) => {
				res.json({response: "Sorry, there was an error..."})
				throw err
			})
		}
	})
	.catch((err) => {
		console.log(err)
	})
}


exports.deleteUser = function (req, res) {
	let usernameToDelete = req.query.username

	if(!usernameToDelete) {
		res.json({response: "Please specify a USERNAME to delete from database"});
		return;
	}

	promises.deleteOne(usernameToDelete)
	.then(() => {
		res.json({response: `User ${usernameToDelete} was successfully deleted!`});
	})
	.catch((err) => {
		console.log(err)
		res.json({response: `Failed to delete the user: ${usernameToDelete}`})
	})
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

	promises.findOne(usernameToUpdate)
	.then((result) => {
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
			promises.updateOne(usernameToUpdate, update)
			.then(() => {
				res.send({response: "Update applied"})
			})
			.catch(() => {
				res.send({response: "Error Applying Update"})
			})
			
		} else {
			res.json({response: `No user with username ${usernameToUpdate} exists in the database`});
			return;
		}
	})
	.catch((e) => {
		console.log(e)
		res.json({response: `Failed to update the user: ${usernameToUpdate}`})
	})
}
