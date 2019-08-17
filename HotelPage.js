'use strict';

var HotelPage = function () {

    var guestField = element(by.css("[id *= roomsGuestsAboveForm]")).element(by.css("[class *= _idj]"));
    var originField = element(by.css("[id *= location-textInputWrapper]"));
    var startDateField = element(by.css("[id *= dateRangeInput-display-start]"));
    var endDateField = element(by.css("[id *= dateRangeInput-display-end]"));

    this.openHomePage = async function () {
        await browser.get(browser.params.kayakSiteLink);
    };

    this.openHotelLink = async function () {
        var link = element(by.linkText(browser.params.hotels));
        await link.click();
    };

    this.getText =  async function (element){
        return await element.getText();
    };

    this.isPresent = async function (element){
        return await element.isPresent();
    }
};
module.exports = new HotelPage();