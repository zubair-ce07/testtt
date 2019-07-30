const passport = require('passport');
const Strategy = require('passport-local').Strategy;
const passwordUtility = require("../helpers/passwordUtility.js");
const connection = require("../database/connect.js");
const model = require("../database/model")

// var collection;

connection.connect(() => {
    console.log("WE ARE CONNECTED")
	// collection = connection.database.collection("users_test");
})


passport.use(new Strategy(
function(username, password, cb) {
	model.Users.findOne({username:username}, function(err, user) {
		if (!user) { return cb(null, false); }
		var givenPassHash = passwordUtility.sha512(password, user.get("password_salt")).passwordHash
		if (err) {return cb(err); }
		if (givenPassHash != user.get("password_hash")) { 
			console.log(givenPassHash);
			return cb(null, false, {message: "Wrong Password!"}); 
		}
		return cb(null, user);
	});
}));


passport.serializeUser(function(user, cb) {
	cb(null, user.get("username"));
});


passport.deserializeUser(function(username, cb) {
	model.Users.findOne({username: username}, function (err, user) {
		if (err) { return cb(err); }
		cb(null, user);
	});
});
