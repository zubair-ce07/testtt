const csv = require('csvtojson')

async function csvToJson(filename) {
    try {
        const result = await csv().fromFile(filename)
        return result
    }
    catch (error) {
        console.error(error)
    }
}

module.exports = csvToJson
