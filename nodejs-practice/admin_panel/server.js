require('dotenv').config();
require("./database/connect.js")

const express = require('express');
const passport = require("passport");
const publicRoutes = require("./routes/publicRoutes.js");
const authenticatedRoutes = require("./routes/authenticatedRoutes.js");
const loginStatus = require('connect-ensure-login');

var app = express();

app.use(express.urlencoded({ extended: true }));
app.use(require('express-session')({  secret: 'keyboard cat',
									  resave: false,
									  saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());

app.use(publicRoutes);
app.use(loginStatus.ensureLoggedIn('/'), authenticatedRoutes);

app.listen(8080);
