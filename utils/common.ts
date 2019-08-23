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

export
{
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS,
    getTimeoutErrorMessage,
    convertMonthNameToShortName
}