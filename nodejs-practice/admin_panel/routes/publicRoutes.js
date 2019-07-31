const express = require("express");
const passport = require("passport");


const Router = express.Router();


Router.get('/', function(req, res) {
	if (req.user) {
		res.json({response: "Hi there! You are now logged in..."})
	} else {
		res.json({response: "Please log in.."});
	}
});


Router.post('/login',
	passport.authenticate('local', { successRedirect: '/', failureRedirect: '/'})
);


Router.get('/logout',
	function(req, res){
		req.logout();
		res.redirect('/');
});


module.exports = Router;
