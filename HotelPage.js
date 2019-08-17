'use strict';

var HotelPage = function () {

    var guestField = element(by.css("[id *= roomsGuestsAboveForm]")).element(by.css("[class *= _idj]"));
    var originField = element(by.css("[id *= location-textInputWrapper]"));
    var originTextBox = element.all(by.css("[id *= textInputWrapper]")).first().element(by.tagName('input'));
    var startDateField = element(by.css("[id *= dateRangeInput-display-start]"));
    var endDateField = element(by.css("[id *= dateRangeInput-display-end]"));
    var searchBtn = element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
    var EC = protractor.ExpectedConditions;

    this.openHomePage = async function () {
        await browser.get(browser.params.kayakSiteLink);
    };

    this.openHotelLink = async function () {
        var link = element(by.linkText(browser.params.hotels));
        await link.click();
    };

    this.getText = async function (element) {
        return await element.getText();
    };

    this.isDisplayed = async function (element) {
        return await element.isDisplayed();
    }

    this.searchHotels = async function () {

        var resultCount = 0;
        var originFieldBox = element.all(by.css("[id *= location-display]")).first();
        browser.wait(EC.visibilityOf(originFieldBox), 3000);
        originFieldBox.click();

        browser.wait(EC.visibilityOf(originTextBox), 7000);
        originTextBox.sendKeys(browser.params.bcnKeys);

        var originList = element.all(by.css("[id *= location-smarty-content]")).first();

        browser.wait(EC.elementToBeClickable(originList), 5000);

        originList.all(by.tagName('li')).first().click();

        await searchBtn.click();
        var resultsContainer = element(by.css("[id = searchResultsList]"));
        browser.wait(EC.presenceOf(resultsContainer), 10000);

        var resultbox = element(by.css("[class *= normalResults]"));
        browser.wait(EC.presenceOf(resultbox), 10000);

        var results = resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
        browser.wait(EC.presenceOf(results), 10000);

        resultCount = await results.count();
        
        return await resultCount
    }
};
module.exports = new HotelPage();