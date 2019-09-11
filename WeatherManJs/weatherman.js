const moment = require("moment");
const csv = require("csvtojson");
const fs = require("fs");
const yargs = require("yargs");
const weatherFiles = fs.readdirSync("weatherfiles")

async function generateYearReport(year) {
  let yearRecords = []
  for (file of weatherFiles) {
    if (file.includes(year)) {
      try {
        var weatherRecords = await readFile(`weatherfiles/${file}`);
      }
      catch (error) {
        console.log(error)
      }
      for (record of weatherRecords) {
        if (record['Max TemperatureC'] && record['Min TemperatureC'] && record['Max Humidity']) {
          yearRecords.push(record)
        }
      }
    }
  }
  if (yearRecords.length == 0) {
    return;
  }
  maxTemp = getMaxTemp(yearRecords)
  minTemp = getMinTemp(yearRecords)
  maxHumid = getMaxHumidty(yearRecords)
  console.log(`Highest: ${maxTemp['Max TemperatureC']}C on ${maxTemp['PKT']}`)
  console.log(`Lowest: ${minTemp['Min TemperatureC']}C on ${minTemp['PKT']}`)
  console.log(`Humidity: ${maxHumid['Max Humidity']}% on ${maxHumid['PKT']}`)
}

async function generateMonthReport(year, month) {
  let monthRecords = []
  month = moment.monthsShort(month - 1)
  for (file of weatherFiles) {
    if (file.includes(`_${year}_${month}`)) {
      try {
        var weatherRecords = await readFile(`weatherfiles/${file}`);
      }
      catch (error) {
        console.log(error)
      }
      for (record of weatherRecords) {
        if (record['Max TemperatureC'] && record['Min TemperatureC'] && record['Mean Humidity']) {
          monthRecords.push(record)
        }
      }
    }
  }
  if (monthRecords.length == 0) {
    return;
  }
  var highestAvg = getHighestAvg(monthRecords)
  var lowestAvg = getLowestAvg(monthRecords)
  var avgHumidity = getAvgHumidity(monthRecords)
  console.log(`Highest Average: ${highestAvg}C`)
  console.log(`Lowest Average: ${lowestAvg}C`)
  console.log(`Average Mean Humidity: ${avgHumidity}%`)
 
}

function getHighestAvg(weatherRecords) {
  var highestAvg = (weatherRecords.reduce(function(previous, current) {
    return previous + +current['Max TemperatureC']
  }, 0) / weatherRecords.length);
  return Math.round(highestAvg)
}

function getLowestAvg(weatherRecords) {
  var lowestAvg = (weatherRecords.reduce(function(previous, current) {
    return previous + +current['Min TemperatureC']
  }, 0) / weatherRecords.length);
  return Math.round(lowestAvg)
}

function getAvgHumidity(weatherRecords) {
  var avgHumidity = (weatherRecords.reduce(function(previous, current) {
    return previous + +current['Mean Humidity']
  }, 0) / weatherRecords.length);
  return Math.round(avgHumidity)
}

function getMaxTemp(weatherRecords) {
  let maxTemp = weatherRecords.reduce(function(previous, current) {
    return (+previous['Max TemperatureC'] > +current['Max TemperatureC']) ? previous : current
})
return maxTemp
}

function getMinTemp(weatherRecords) {
  let minTemp = weatherRecords.reduce(function(previous, current) {
    return (+previous['Min TemperatureC'] < +current['Min TemperatureC']) ? previous : current
})
return minTemp
}

function getMaxHumidty(weatherRecords) {
  let maxHumid = weatherRecords.reduce(function(previous, current) {
    return (+previous['Max Humidty'] > +current['Max Humidity']) ? previous : current
})
return maxHumid
}

async function readFile(filename) {
  try {
    const result = await csv().fromFile(filename);
    return result;
  }
  catch (error) {
    console.error(error)
  }
}

function isValidYear(year) {
  if (year === undefined || year < 2000 || year > 2100) {
    console.error('Please specify a valid year!')
    return false;
  }
  return true;
}

function isValidMonth(month) {
  if (month === undefined || month < 1 || month > 12) {
    console.error('Please specify a valid month!')
    return false;
  }
  return true;
}

function parseArguments() {
  yargs.command(
    ['yearly', '-y'],
    'Generate yearly report',
    yargs => {
      yargs.positional('year', {
        describe: 'Year for which report should be generated',
        type: 'number'
      });
    },
    argv => {
      if (isValidYear(argv.year)) {
        generateYearReport(argv.year)
      }
      
    }
  );
  
  yargs.command(
    ['monthly'],
    'Generate monthly average report',
    yargs => {
      yargs.positional('year', {
        describe: 'Year for which average should be calculated',
        type: 'number'
      });
      yargs.positional('month', {
        describe: 'Month of year for which average should be calculated',
        type: 'number'
      });
    },
    argv => {
     if (isValidYear(argv.year) && isValidMonth(argv.month)) {
      generateMonthReport(argv.year, argv.month)
     }
      
    }
  );
  yargs.parse();
}

parseArguments()