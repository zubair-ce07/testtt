const mongo = require("../database/connect.js");

var collection;

mongo.connect((err) => {
	if (err) throw err
	collection = mongo.database.collection("users_test");
})


exports.findAll = () => {
    return new Promise((resolve, reject) => {
        collection.find({}, {projection:{_id: 0, password_salt: 0, password_hash: 0}}, (err, result) => {
            if (err) reject(err);
            resolve(result)
        })
    })
    
}

exports.findOne = (username) => {
    return new Promise((resolve, reject) => {
        collection.findOne({username: username}, (err, result) => {
            if (err) reject(err)
            resolve(result)
        })
    })
}

exports.updateOne = (username, update) => {
    return new Promise((resolve, reject) => {
        collection.updateOne({username: username}, {$set: update}, (err, result) => {
            if (err) reject(err)
            resolve(result)
        })
    })
}


exports.insertOne = (userDetails, passwordObject) => {
    return new Promise((resolve, reject) => {
        collection.insertOne({
            username: userDetails.username, 
            name: userDetails.name, 
            admin: userDetails.admin, 
            password_hash: passwordObject.passwordHash, 
            password_salt: passwordObject.salt}, (err) => {
                if (err) reject(err)
                resolve()
            })
    })
}

exports.deleteOne = (username) => {
    return new Promise((resolve, reject) => {
        collection.deleteOne({username: username}, (err) => {
            if (err) reject(err)
            resolve()
        })
    })
}
