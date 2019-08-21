var controllers = require.main.require("./src/controllers");
var database = require.main.require('./src/database');

controllers.saveConfiguration = function (req, res, callback) {
        /**
         * save configuration from edX
         * ***/
        var requestBody = req.body;
        var db = database.client.collection("configuration");


        if (requestBody != null) {
            if(requestBody.philu_config != null){
                try {
                    var configuration = JSON.parse(requestBody.philu_config)
                } catch (e) {
                    res.status(400).json({e});
                    return
                }
    
                db.findOne({"key": "badge"}, function (err, response) {
                    if (err) {
                        res.status(400).json({message: err.message});
                    } else if (!response) {
                        db.insert(configuration, function (err, response) {
                            if(err) {
                                res.status(400).json({message: err.message});
                            } else {
                                res.status(200).json({message: "configuration saved successfully"});
                            }
                        })
                    } else {
                        db.replaceOne({"key": "badge"}, configuration, function(err, response) {
                            if (err) {
                                res.status(400).json({message: err.message});
                            } else {
                                res.status(200).json({message: "configuration replaced successfully"});
                            }
                        })
                    }
                })

            } else{
                res.status(400).json({message: "Please use `philu_config` key to send data"});
            }
        } else {
            res.status(400).json({message: "Please send some data for configuration"});
        }
};

module.exports = controllers;
