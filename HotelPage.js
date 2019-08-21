'use strict';
var HotelPage = function () {
    var guestField;
    var originField;
    var startDateField;
    var endDateField;

    this.openHomePage = async function () {
        await browser.get(browser.params.kayakSiteLink);
    };
    var EC = protractor.ExpectedConditions;
    var error;
    this.openHotelLink = async function () {
        var link = element(by.linkText(browser.params.hotels));
        await link.click();
    };

    this.getFieldText = function () {

        return this.guestField.getText();
    };

    this.setElement = function (elem) {
        switch (elem) {
            case "guestField":
                this.guestField = element.all(by.css("[id *= roomsGuestsAboveForm]")).first().element(by.css("[class *= _idj]"));
                break;
            case "originField":
                this.originField = element.all(by.css("[id *= location-display]")).first();
                break;
            case "startDateField":
                this.startDateField = element.all(by.css("[id *= dateRangeInput-display-start]")).first();
                break;
            case "endDateField":
                this.endDateField = element.all(by.css("[id *= dateRangeInput-display-end]")).first();
                break;
            case "originTextBox":
                this.originTextBox = element.all(by.css("[id *= location-textInputWrapper]")).first().element(by.tagName('input'));
                break;
        }
    }
    var originTextBox;
    this.setKeysinOriginField = async function () {
        var originFieldBox = element.all(by.css("[id *= location-display]")).first();
        browser.wait(EC.visibilityOf(originFieldBox), 3000);
        originFieldBox.click();
        await this.setElement("originTextBox"); 
        browser.wait(EC.visibilityOf(this.originTextBox), 7000);
        await this.originTextBox.sendKeys(browser.params.bcnKeys);
    }

    this.searchHotels = async function () {

        var originList = element.all(by.css("[id *= location-smarty-content]")).first();
        browser.wait(EC.elementToBeClickable(originList), 5000);
        originList.all(by.tagName('li')).first().click();
        var searchBtn = element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
        await searchBtn.click();
    }
};
module.exports = new HotelPage();