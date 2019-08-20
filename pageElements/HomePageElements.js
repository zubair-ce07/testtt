"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
class HomePageElements {
    constructor() {
        this.flightOrigin = protractor_1.element(protractor_1.by.name('origin'));
        this.flightDestination = protractor_1.element(protractor_1.by.name('destination'));
        this.flightDepartureDate = protractor_1.element(protractor_1.by.css("div[id*='-dateRangeInput-display-start-inner']"));
        this.flightReturnDate = protractor_1.element(protractor_1.by.css("div[id*='-dateRangeInput-display-end-inner']"));
        this.flightTravelers = protractor_1.element(protractor_1.by.css("a[id*='-travelers-dialog']")).element(protractor_1.by.css('.label'));
        this.mainGraph = protractor_1.element(protractor_1.by.css('.graph-grid'));
        this.searchBtn = protractor_1.element(protractor_1.by.css("button[aria-label='Edit search']"));
        this.allVisibleGraphs = protractor_1.element.all(protractor_1.by.css('.graph-col'));
        this.newCalendarDate = protractor_1.element(protractor_1.by.css("div[aria-label='September 10']"));
        this.graphBar = protractor_1.element(protractor_1.by.css("button[data-date='2019-08-29']"));
        this.selectedGraphBar = protractor_1.element(protractor_1.by.css('.Button-No-Standard-Style.js-bar.item.selected'));
        this.graphBarTooltip = this.graphBar.element(protractor_1.by.css('.bar')).element(protractor_1.by.css('.price-info')).element(protractor_1.by.css('.price-price'));
        this.selectedGraphBarPrice = protractor_1.element(protractor_1.by.css('.highlight-price'));
        this.selectedPriceLabel = protractor_1.element(protractor_1.by.css('.hightlight'));
        this.searchTheseDaysBtn = protractor_1.element(protractor_1.by.css("a[aria-describedby*='-search-dates-description']"));
        this.showDetailsBtn = protractor_1.element(protractor_1.by.css("a[id*='-extra-info-details-link-toggleMore']"));
        this.allDetailsPanel = protractor_1.element.all(protractor_1.by.css("div[class='resultInner']"));
        this.allDetailsPanelDates = protractor_1.element.all(protractor_1.by.css('.leg-dates-set'));
    }
    getFlightOrigin() {
        return this.flightOrigin.getAttribute('value');
    }
    getFlightDestination() {
        return this.flightDestination.getAttribute('value');
    }
    getFlightDepartureDaten() {
        return this.flightDepartureDate.getText();
    }
    getFlightReturnDate() {
        return this.flightReturnDate.getText();
    }
    getFlightTravelers() {
        return this.flightTravelers.getText();
    }
    getGraph() {
        return this.mainGraph;
    }
    clickSearchBtn() {
        this.searchBtn.click();
    }
    getAllVisibleGraphs() {
        return this.allVisibleGraphs;
    }
    clickFlightReturnDate() {
        this.flightReturnDate.click();
    }
    getNewCalendarDate() {
        return this.newCalendarDate;
    }
    clickNewCalendarDate() {
        this.getNewCalendarDate().click();
    }
    hoverOverGraphBar() {
        protractor_1.browser.actions().mouseMove(this.graphBar).perform();
    }
    getGraphBarTooltip() {
        return this.graphBarTooltip;
    }
    getSelectedGraphBar() {
        return this.selectedGraphBar;
    }
    getSelectedGraphBarDate() {
        return this.selectedGraphBar.getAttribute('data-date');
    }
    getNewGraphBar(barDate) {
        return protractor_1.element(protractor_1.by.css("button[data-date='" + barDate + "']"));
    }
    getSelectedBarPrice() {
        return this.selectedGraphBarPrice;
    }
    getSelectedPriceLabel() {
        return this.selectedPriceLabel;
    }
    getSearchTheseDaysBtn() {
        return this.searchTheseDaysBtn;
    }
    clickSearchTheseDaysBtn() {
        this.searchTheseDaysBtn.click();
    }
    getShowDetailsBtn() {
        return this.showDetailsBtn;
    }
    clickShowDetailsBtn() {
        this.showDetailsBtn.click();
    }
    getDetailsPanel() {
        return this.allDetailsPanel;
    }
    getDetailsPanelDepartureDate() {
        return this.allDetailsPanelDates.first();
    }
}
exports.default = HomePageElements;
