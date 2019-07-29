const passport = require('passport');
const Strategy = require('passport-local').Strategy;
const passwordUtility = require("../helpers/passwordUtility.js");
const mongo = require("./connect.js")

var db;

mongo.connect((err) => {
	if (err) throw err
	db = mongo.db.db("users_test").collection("users_test");
})


passport.use(new Strategy(
function(username, password, cb) {
	db.findOne({username:username}, function(err, user) {
		if (!user) { return cb(null, false); }
		given_password_hash = passwordUtility.sha512(password, user.password_salt).passwordHash
		if (err) {return cb(err); }
		if (given_password_hash != user.password_hash) { 
			console.log(given_password_hash);
			return cb(null, false, {message: "Wrong Password!"}); 
		}
		return cb(null, user);
	});
}));


passport.serializeUser(function(user, cb) {
	cb(null, user.username);
});


passport.deserializeUser(function(username, cb) {
	db.findOne({username: username}, function (err, user) {
		if (err) { return cb(err); }
		cb(null, user);
	});
});
