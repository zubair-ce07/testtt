var controllers = require.main.require("./src/controllers");

const {
    BADGE_CONFIG_KEY, 
    BADGE_TYPES
} = require('../constants');

const {
	dbFindOne,
	dbUpdate,
    dbDeleteConfig,
    dbCount,
    dbInsert
} = require('./dataLayerOps');


const initializeConfigCollection = function () {

    dbCount({ key: BADGE_CONFIG_KEY })
    .then((countResult) => {
        if (countResult) {
            return "Already configured"
        } else {
            dbInsert({ key: BADGE_CONFIG_KEY, value: {} })
            .then((insertionResult) => {
                if (insertionResult) {
                    return "Configuration successful"
                } else {
                    throw Error("Error", "Unknown insertion error occurredoccurred during configuration!")
                }
            })
        }
    })
    .catch((error) => {
        throw Error("Error", "Unknown count error occurred during configuration!")
    })
}


const getAllConfig = function (req, res) {
    /**
     * Return badging configuration from database
     * ***/

    dbFindOne({key: BADGE_CONFIG_KEY})
    .then((badgingConfig) => {
        if (badgingConfig) {
            return res.status(200).json(badgingConfig);
        } else {
            return {}
        }
    })
    .catch((error) => {
        return res.status(500).json({ message: err.message });
    })
}


const updateConfigById = function (req, res) {
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

    dbUpdate(badgeId, type, threshold)
    .then((updateResult) => {
        return res.status(200).json({ message: "Key updated successfully!" });
    })
    .catch((err) => {
        return res.status(500).json({ message: err.message });
    })
};


const deleteConfigById = function (req, res) {
    /**
     * delete configuration from database by badgeID
     * ***/

    const { badgeId } = req.params;

    dbDeleteConfig(badgeId)
    .then((deleteResult) => {
        console.log(deleteResult, typeof deleteResult)
        if (deleteResult) {
            return res.status(200).json({ message: 'Key deleted successfully!' });
        } else {
            return res.status(204);
        }
    })
    .catch((err) => {
        return res.status(500).json({ message: err.message });
    })
};


module.exports = {
	initializeConfigCollection,
    getAllConfig,
    updateConfigById,
    deleteConfigById
};
