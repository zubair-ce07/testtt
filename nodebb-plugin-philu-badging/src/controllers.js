//var controllers = require.main.require("./src/controllers");

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


const initializeConfigCollection = async function () {
    /**
     * Initialize the configuration collection in database
     * ***/

    try {
        let countResult = await dbCount({ key: BADGE_CONFIG_KEY })
        if (countResult) {
            return "Already configured"
        } else {
            try {
                let insertionResult = await dbInsert({ key: BADGE_CONFIG_KEY, value: {} })
                if (insertionResult) {
                    return "Configuration successful"
                }
            } catch(e) {
                throw Error("Error", "Unknown insertion error occurred during configuration!")
            }
        }
    } catch(e) {
        throw Error("Error", "Unknown count error occurred during configuration!")
    }
}


const getAllConfig = async function (req, res) {
    /**
     * Return badging configuration from database
     * ***/

    try {
        let badgingConfig = await dbFindOne({key: BADGE_CONFIG_KEY})
        if (badgingConfig) {
            return res.status(200).json(badgingConfig);
        } else {
            return res.status(204).json({});
        }
    } catch (e){
        res.status(500).json({ message: e.message });
        throw e;
    }
}


const updateConfigById = async function (req, res) {
    /**
     * save configuration to database by badgeID
     * ***/
    
    const { badgeId } = req.params;
    const { type, threshold } = req.body;

    if(!badgeId) {
        return res.status(400).json({
            message: 'Required parameters are missing',
            requiredParams: ['badgeId', 'type', 'threshold']
        });
    }

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

    try {
        await dbUpdate(badgeId, type, threshold);
        return res.status(200).json({ message: "Key updated successfully!" });
    } catch (e) {
        return res.status(500).json({ message: e.message });
    }
};


const deleteConfigById = async function (req, res) {
    /**
     * delete configuration from database by badgeID
     * ***/

    const { badgeId } = req.params;

    try {
        let deleteResult = await dbDeleteConfig(badgeId);
        
        if(deleteResult){
            return res.status(200).json({ message: 'Key deleted successfully!' });
        } else {
            return res.status(204).end();
        }
    } catch(err) {
        return res.status(500).json({ message: err.message });
    }
};


module.exports = {
	initializeConfigCollection,
    getAllConfig,
    updateConfigById,
    deleteConfigById
};
