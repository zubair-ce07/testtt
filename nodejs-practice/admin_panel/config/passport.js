const passport = require('passport');
const Strategy = require('passport-local').Strategy;
const passwordUtility = require("../helpers/passwordUtility.js");
const model = require("../database/model")

passport.use(new Strategy(
	
function(username, password, callback) {
	model.Users.findOne({username:username})
	.then(user => {
		if (!user) { return callback(null, false); }
		var givenPassHash = passwordUtility.sha512(password, user.get("password_salt")).passwordHash
		if (givenPassHash != user.get("password_hash")) { 
			console.log(givenPassHash);
			return callback(null, false, {message: "Wrong Password!"}); 
		}
		return callback(null, user);
	})
	.catch(err => {
		return callback(err)
	})
}));


passport.serializeUser(function(user, callback) {
	callback(null, user.get("username"));
});


passport.deserializeUser(function(username, callback) {

	model.Users.findOne({username: username})
	.then(user => {
		callback(null, user);
	})
	.catch(err => {
		return callback(err)
	})

});
