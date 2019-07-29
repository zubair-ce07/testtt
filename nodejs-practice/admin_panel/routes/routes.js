const express = require("express");
const loginStatus = require('connect-ensure-login');
const passport = require('passport');
const controllers = require("../controllers/controllers.js");


const Router = express.Router();

Router.get('/', function(req, res) {
	if (req.user) {
		res.json({response: "Hi there! You are now logged in..."})
	} else {
		res.json({response: "Please log in.."});
	}
});


Router.post('/login',
	passport.authenticate('local', { failureRedirect: '/'}),
	function(req, res) {
		res.redirect('/');
});


Router.get('/viewUsers', 
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.viewUsers(req, res)
});


Router.post('/addUser',
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.addUser(req, res)
})

Router.put('/updateUser',
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.updateUser(req, res)
})

Router.patch('/updateUser',
	loginStatus.ensureLoggedIn('/'),
	function(req, res) {
		controllers.updateUser(req, res);
})

Router.get('/logout',
	function(req, res){
		req.logout();
		res.redirect('/');
});

Router.delete('/deleteUser', 
	loginStatus.ensureLoggedIn('/'),
	function (req, res) {
		controllers.deleteUser(req, res);
})


Router.get('/profile',
	loginStatus.ensureLoggedIn('/'),
	function(req, res) {
		controllers.showProfile(req, res);
})

module.exports = Router;
