const mongoose = require("mongoose")
const connection = require("./configuration.js")
const models = require("./model.js")

mongoose.connection.on('error', console.error.bind(console, 'connection error:'));

module.exports.connect = function connect(cb) {
    mongoose.connection.once('open', function() {
        cb()
    });
}
