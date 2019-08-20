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

export
{
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS,
}