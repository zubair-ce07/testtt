import { protractor, browser, element, by } from "protractor";

function waitForElementPresence(elementSelector, timeout, error) {
    let EC = protractor.ExpectedConditions;
    browser.wait(EC.presenceOf(elementSelector), timeout, error);
}

function waitForElementVisibility(elementSelector, timeout, error) {
    let EC = protractor.ExpectedConditions;
    browser.wait(EC.visibilityOf(elementSelector), timeout, error);
}

function getElementByCSS(selector) {
    return element(by.css(selector));
}

function getTimeoutErrorMessage(sectionName) {
    return `Timeout Error! ${sectionName} is taking too long to appear in DOM`;
}

function convertMonthNameToShortName(monthFullName) {
    const shortMonths = {
        'January': 'Jan',
        'February': 'Feb',
        'March': 'Mar',
        'April': 'Apr',
        'May': 'May',
        'June': 'Jun',
        'July': 'Jul',
        'August': 'Aug',
        'September': 'Sep',
        'October': 'Oct',
        'November': 'Nov',
        'December': 'Dec'
    };
    return shortMonths[monthFullName];
}

function convertShortMonthNameToMonthNumber(monthShortName) {
    const monthNo = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    };
    return monthNo[monthShortName];
}

function convertDateInFormatMonthInNumberSlashDayInNumber(dateInFormatMonthSpaceDay) {
    const dateParts = dateInFormatMonthSpaceDay.split(" ");
    const shortMonthName = dateParts[0];
    const monthInNumber = convertShortMonthNameToMonthNumber(shortMonthName);
    return `${monthInNumber}/${dateParts[1]}`;
}

function convertTimeToMinutes(timeIn12HourFormat) {
    const time = timeIn12HourFormat.match(/(\d+):(\d+) (\w)/);
    const hours = Number(time[1]);
    const minutes = Number(time[2]);
    const meridian = time[3].toLowerCase();
    let hoursIn24HourFormat = hours;
    if (meridian == 'p' && hours < 12) {
        hoursIn24HourFormat = hours + 12;
    }
    else if (meridian == 'a' && hours == 12) {
        hoursIn24HourFormat = hours - 12;
    }

    return (hoursIn24HourFormat * 60) + minutes;
}

export
{
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS,
    getTimeoutErrorMessage,
    convertMonthNameToShortName,
    convertShortMonthNameToMonthNumber,
    convertDateInFormatMonthInNumberSlashDayInNumber,
    convertTimeToMinutes
}