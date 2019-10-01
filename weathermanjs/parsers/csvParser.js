import csv from 'csvtojson';

export let parseCSVFiles = async (path, fileNames) => {
    let records = [];
    for (let fileName of fileNames) {
        let filePath = `${path}${fileName}`;
        records = [...records ,...(await csv().fromFile(filePath))];
    }
    return records;
};