const csv = require('csvtojson')

var csvToJson = async filename => {
    try {
        const result = await csv().fromFile(filename)
        return result
    }
    catch (error) {
        console.error(error)
    }
}

module.exports = csvToJson
