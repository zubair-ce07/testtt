var mongoose = require('mongoose');


const uri = `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_CLUSTER}`;
const options = {useNewUrlParser: true, dbName: "users_test"}

const client = mongoose.connect(uri, options);

module.exports = client;
