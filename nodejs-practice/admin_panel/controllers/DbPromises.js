const model = require("../database/model");
const ObjectID = require('mongodb').ObjectID;


exports.findAll = () => {
    return new Promise((resolve, reject) => {
        model.Users.find({}, "-_id -password_salt -password_hash").lean().exec((err, result) => {
            if (err) reject(err);
            resolve(result)
        })
    })
    
}

exports.findOne = (username) => {
    return new Promise((resolve, reject) => {
        model.Users.findOne({username: username})
        .then ((result) => {
            resolve(result)
        })
        .catch((err) => {
            reject(err)
        })
    })
}


exports.updateOne = (username, update) => {
    return new Promise((resolve, reject) => {
        model.Users.updateOne({username: username}, update, (err, result) => {
            if (err) reject(err)
            resolve(result)
        })
    })
}


exports.insertOne = (userDetails, passwordObject) => {
    return new Promise((resolve, reject) => {
        new model.Users({
                        _id: new ObjectID(),
                        username: userDetails.username, 
                        name: userDetails.name, 
                        admin: userDetails.admin, 
                        password_hash: passwordObject.passwordHash, 
                        password_salt: passwordObject.salt}).save()
        .then(() => {
            resolve()
        })
        .catch(err => {
            reject (err)
        })
    })
}

exports.deleteOne = (username) => {
    return new Promise((resolve, reject) => {
        model.Users.deleteOne({username: username})
        .then(() => {
            resolve()
        })
        .catch((err) => {
            reject(err)
        })
    })
}
