const express = require("express");
const controllers = require("../controllers/controllers.js");


const Router = express.Router();


Router.get('/viewUsers', 
	function (req, res) {
		controllers.viewUsers(req, res)
});


Router.post('/addUser',
	function (req, res) {
		controllers.addUser(req, res)
})


Router.put('/updateUser',
	function (req, res) {
		controllers.updateUser(req, res)
})


Router.patch('/updateUser',
	function(req, res) {
		controllers.updateUser(req, res);
})


Router.delete('/deleteUser',
	function (req, res) {
		controllers.deleteUser(req, res);
})


Router.get('/profile',
	function(req, res) {
		controllers.showProfile(req, res);
})


module.exports = Router;
