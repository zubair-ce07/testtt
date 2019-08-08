exports.waitForElementPresence = function(elementSelector, timeout, error) {
    var EC = protractor.ExpectedConditions;
    browser.wait(EC.presenceOf(element(by.css(elementSelector))), timeout, error);
};

exports.waitForElementVisibility = function(elementSelector, timeout, error) {
    var EC = protractor.ExpectedConditions;
    browser.wait(EC.visibilityOf(element(by.css(elementSelector))), timeout, error);
};

exports.handleException = function(functionName, errMsg, context = []) {
    console.log(`function ${functionName} > Exception message`, errMsg);
}
