var db = require.main.require('./src/database').client.collection("configuration");

const {
    BADGE_CONFIG_KEY
} = require('../constants');

var utils = module.exports

utils.initializeConfigCollection = function () {
    new Promise(async (resolve, reject) => {
        if (await db.count({ key: BADGE_CONFIG_KEY })) {
            return resolve();
        }
        
        resolve(await db.insert({
            key: BADGE_CONFIG_KEY,
            value: {}
        }));
    })
    .then((message) => {
        return message
    })
}
