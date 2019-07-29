const express = require("express");
const loginStatus = require('connect-ensure-login');
const passport = require('passport');
const controllers = require("./controllers.js");


const Router = express.Router();

Router.get('/', function(req, res) {
	if (req.user) {
		res.json({response: "Hi there! You are now logged in..."})
	} else {
		res.json({response: "Please log in.."});
	}
});


Router.post('/',
	passport.authenticate('local', { failureRedirect: '/'}),
	function(req, res) {
		res.redirect('/');
});


Router.get('/viewUsers', function (req, res) {
	controllers.viewUsers(req, res)
});


Router.put('/',
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.addUser(req, res)
})


Router.get('/logout',
	function(req, res){
		req.logout();
		res.redirect('/');
});


Router.patch('/',
	function(req, res) {
		controllers.updateUser(req, res);
})


Router.delete('/', 
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.deleteUser(req, res);
})


Router.get('/profile',
	loginStatus.ensureLoggedIn('/'),
	function(req, res) {
		let user = req.user;
		res.json({userDetails: {
			id: user.id,
			username: user.username,
			name: user.name,
			admin: user.admin
		}
	});
});

module.exports = Router;
