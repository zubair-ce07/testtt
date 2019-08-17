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

function getAllElementByCSS(selector) {
    return element.all(by.css(selector));
}

export
{
    waitForElementPresence,
    waitForElementVisibility,
    getElementByCSS,
    getAllElementByCSS
}