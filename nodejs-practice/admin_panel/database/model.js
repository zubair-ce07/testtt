var mongoose = require('mongoose');
var ObjectID = require('mongodb').ObjectID;

var userSchema = new mongoose.Schema({
    _id: ObjectID,
    username: String,
    name: String,
    admin: String,
    password_hash: String,
    password_salt: String
}, {versionKey: false});

exports.Users = mongoose.model('users_test', userSchema, 'users_test');
