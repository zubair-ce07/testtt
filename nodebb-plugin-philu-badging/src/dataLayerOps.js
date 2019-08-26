var db = require.main.require('./src/database').client.collection("configuration");

const {
    BADGE_CONFIG_KEY,
} = require('../constants');


const dbFindOne = async (query) => {
    try {
        return await db.findOne(query);
    } catch (error) {
        return error;
    }
}


const dbUpdate = async (badgeId, type, threshold) => {
    try {
        const updateObj = { $set: {} };
        updateObj.$set[`value.${badgeId}`] = { type, threshold };
        return await db.update({ key: BADGE_CONFIG_KEY }, updateObj);
    } catch (error) {
        return error
    }
}


const dbDeleteConfig = async (badgeId) => {
    try {
        const updateObj = { $unset: {} };
        updateObj.$unset[`value.${badgeId}`] = '';
        let {
            result: { nModified }
        } = await db.update(
            { key: BADGE_CONFIG_KEY },
            updateObj
        );
        return nModified;
    } catch (error) {
        return error;
    }
}

const dbCount = async (countKey) => {
    try {
        return await db.count(countKey)
    } catch (error) {
        return error;
    }
}

const dbInsert = async (insertObj) => {
    try {
        return await db.insert(insertObj)
    } catch (error) {
        return error;
    }
}

module.exports = {
	dbFindOne,
	dbUpdate,
    dbDeleteConfig,
    dbCount,
    dbInsert,
};
