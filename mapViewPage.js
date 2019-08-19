'use strict';
var mapViewPage = function () {
    var mapBtn;

    this.setElement = function (elem) {
        switch (elem) {
            case "mapBtn":
                this.mapBtn = mapView.element(by.css(".showMap"));
                break;
        }

    }
    this.getElement = function (elem) {
        switch (elem) {
            case "mapBtn":
                return this.mapBtn;
        }

    }
    this.isDisplayed = function (elem) {
        try {
            return elem.isDisplayed();
        } catch (error) {
            console.log(error);
        }

    }
    this.displayMapView = async function () {

        var mapView = element.all(by.css("[class *= filterListContainer]")).first();
        this.setElement("mapBtn");
        await mapBtn.click()
    }
}
module.exports = new mapViewPage();