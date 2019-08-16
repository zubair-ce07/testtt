export function waitForElementPresence(elementSelector, timeout, error) {
    let EC = protractor.ExpectedConditions;
    browser.wait(EC.presenceOf(elementSelector), timeout, error);
}

export function waitForElementVisibility(elementSelector, timeout, error) {
    let EC = protractor.ExpectedConditions;
    browser.wait(EC.visibilityOf(elementSelector), timeout, error);
}

export function handleException(functionName, errMsg) {
    console.log(`function ${functionName} > Exception message`, errMsg);
}

export function getAllElementByCSS(selector) {
    return element.all(by.css(selector));
}

export function getSingleElementByCSS(selector) {
    return element(by.css(selector));
}