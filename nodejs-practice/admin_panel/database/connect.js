const mongoose = require("mongoose")

const uri = `mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_CLUSTER}`;
const options = {useNewUrlParser: true, dbName: "users_test"}

mongoose.connect(uri, options)
.then(() => {
    console.log("Connected to the database...")
})
.catch((err) => {
    console.log("ConnectionError: ", err);
})
