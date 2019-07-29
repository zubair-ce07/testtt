const connection = require("./configuration.js")

module.exports.connect = function connect(cb) {
    connection.connect(err => {
        if (err) throw err;
        module.exports.database = connection.db("users_test")
        cb(err);
    });
}
