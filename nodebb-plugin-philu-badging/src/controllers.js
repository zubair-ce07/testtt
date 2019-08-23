var controllers = require.main.require("./src/controllers");
var db = require.main.require('./src/database').client.collection("configuration");

const {
    BADGE_CONFIG_KEY, 
    BADGE_TYPES
} = require('../constants');


controllers.getAllConfig = function (req, res, callback) {
    /**
     * Return badging configuration from database
     * ***/
    new Promise ( async (resolve, reject) => {
        let badgingConfig = await db.findOne({key: BADGE_CONFIG_KEY});

        if(badgingConfig) {
            resolve(badgingConfig)
        } else {
            resolve({})
        }
    })
    .then((badgingConfig) => {
        return res.status(200).json(badgingConfig);
    })
    .catch((err) => {
        return res.status(500).json({ message: err.message });
    })
}

controllers.updateConfigById = function (req, res, callback) {
    /**
     * save configuration to database by badgeID
     * ***/
    const { badgeId } = req.params;
    const { type, threshold } = req.body;

    if (!type || !threshold) {
        return res.status(400).json({
            message: 'Required parameters are missing',
            requiredParams: ['badgeId', 'type', 'threshold']
        });
    }

    const possibleTypeValues = Object.values(BADGE_TYPES);
    if (!possibleTypeValues.includes(type)) {
        return res.status(400).json({
            message: 'Invalid badge type',
            possibleTypeValues
        });
    }

    new Promise ( async (badgeId, type, threshold) => {
        const updateObj = { $set: {} };
        updateObj.$set[`value.${badgeId}`] = { type, threshold };
        await philuConfig.update({ _key: BADGE_CONFIG_KEY }, updateObj);
        resolve()
    })
    .then((badgingConfig) => {
        return res.status(200);
    })
    .catch((err) => {
        return res.status(500).json({ message: err.message });
    })

    callback();
};

controllers.deleteConfigById = function (req, res, callback) {
    /**
     * delete configuration from database by badgeID
     * ***/

    const { badgeId } = req.params;

    new Promise ( async (badgeId) => {
        const updateObj = { $unset: {} };
        updateObj.$unset[`value.${badgeId}`] = '';
        let {
            result: { nModified }
        } = await philuConfig.update(
            { _key: BADGE_CONFIG_KEY },
            updateObj
        );
        resolve(!!nModified);
    })
    .then((keyRemoved) => {
        if(keyRemoved) {
            return res.status(200);
        }
        return res.status(204).json({
            message: 'No config found against this ID'
        });
    })
    .catch((err) => {
        return res.status(500).json({ message: err.message });
    })

    callback();
};

module.exports = controllers;
