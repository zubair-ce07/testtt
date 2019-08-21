'use strict';
var mapViewPage = function () {
    var mapBtn;
    var mapContainer
    var selectedHotel;
    var mapView;

    this.setElement = function (elem) {
        switch (elem) {
            case "mapView":
                this.mapView = element.all(by.css("[class *= filterListContainer]")).first();
                break;
            case "mapBtn":
                this.mapBtn = this.mapView.element(by.css(".showMap"));
                break;
            case "mapContainer":
                this.mapContainer = element.all(by.css("[class *= rail-map-container")).first();
                break;
        }

    }
    var EC = protractor.ExpectedConditions;
    var error;
    this.getMapView = async function () {

        this.setElement("mapView");
        this.setElement("mapBtn");
        await mapBtn.click();
        this.setElement("mapContainer");
        browser.wait(EC.elementToBeClickable(this.mapContainer), 10000);
        return mapContainer.isDisplayed();
    }

    this.getHotelSummaryCard = async function () {

        browser.wait(EC.visibilityOf(this.mapContainer.element(by.css(".gm-style"))), 15000);
        var hotelMarker = mapContainer.all(by.css(".hotel-marker"));
        this.selectedHotel = hotelMarker.first();
        hotelMarker.each(async function (elem, index) {
            var topValue = await elem.getCssValue("top")
            if (topValue > 0) {

                this.selectedHotel = elem;
                await browser.actions().mouseMove(this.selectedHotel).mouseMove(this.selectedHotel).perform()
                var hotelId = await this.selectedHotel.getAttribute("id");
                var id = hotelId.substring(hotelId.indexOf('-'), hotelId.length);
                var cardId = 'summaryCard' + id;
                var summaryCard = element(by.css("[id *= " + cardId + "]"));
            }
        });
        return this.selectedHotel.isDisplayed();
    }

    this.getHotelDetailCard = async function () {

        await browser.actions().mouseMove(this.selectedHotel).mouseMove(this.selectedHotel).click().perform();
        var detailCardContainer = element.all(by.css("[class *= resultWrapper]")).first();
        browser.wait(EC.visibilityOf(detailCardContainer), 10000);
        var detailCard = detailCardContainer.all(by.css("[id *= mainItemWrapper]")).first();
        browser.wait(EC.visibilityOf(detailCard), 10000);
        return detailCard.isDisplayed();
    }

    this.getDealsWindow = async function () {

        var dealBtn = element.all(by.css("[id *= bookButton]")).first();
        await dealBtn.click()
        var handles = await browser.getAllWindowHandles();
        newWindowHandle = handles[1];
        await browser.switchTo().window(newWindowHandle)
        return (browser.getCurrentUrl()).isDisplayed();
    }
}
module.exports = new mapViewPage();