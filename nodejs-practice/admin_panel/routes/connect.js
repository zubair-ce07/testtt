const connection = require("../database/db")

module.exports.connect = function connect(cb) {
    connection.connect(err => {
        if (err) throw err;
        module.exports.db = connection
        cb(err);
    });
}
