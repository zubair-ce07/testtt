require('dotenv').config();
require("./database/connect.js")

const express = require('express');
const passport = require("passport");
const routes = require("./routes/routes.js")

var app = express();

app.use(express.urlencoded({ extended: true }));
app.use(require('express-session')({  secret: 'keyboard cat',
									  resave: false,
									  saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());
app.use(routes)

app.listen(8080);
