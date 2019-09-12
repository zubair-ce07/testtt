const csv = require('csvtojson')

const csvToJson = async filename => {
    try {
        const result = await csv().fromFile(filename)
        return result
    }
    catch (error) {
        console.error(error)
    }
}

module.exports = csvToJson
