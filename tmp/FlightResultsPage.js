"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const CommonPage_1 = require("./CommonPage");
const kayakHelper_1 = require("./kayakHelper");
class FlightResultsPage {
    constructor() {
        this.kayakCommonPage = new CommonPage_1.CommonPage();
        this.helper = new kayakHelper_1.kayakHelper();
        this.expectedCondition = protractor_1.protractor.ExpectedConditions;
        this.kayakUrl = "https://www.kayak.com/flights/NYC-LAX/2019-08-18/2019-08-25";
        this.loadingClass = protractor_1.element(protractor_1.by.css("div[class*=no-spin]"));
        this.flightPredictionGraph = protractor_1.element(protractor_1.by.css("div[class*='FlightQueryPricePrediction'] div[id$=advice]"));
        this.cheapestPriceTab = protractor_1.element(protractor_1.by.css("a[id$='price_aTab']"));
        this.flightCount = protractor_1.element(protractor_1.by.css("div[id$=resultsCount]"));
        this.flightCountLink = protractor_1.element(protractor_1.by.css("div[id$=resultsCount] .showAll"));
        this.flightsTotalCount = protractor_1.element(protractor_1.by.css("span[id$=counts-totalCount]"));
        this.stopsFilter = protractor_1.element.all(protractor_1.by.css("div[id$=stops-content] li"));
        this.airlinesFilter = protractor_1.element.all(protractor_1.by.css("div[id$=airlines-airlines-content] li"));
        this.bookingProvidersFilter = protractor_1.element.all(protractor_1.by.css("div[id$=providers-content] li"));
        this.cabinFilter = protractor_1.element.all(protractor_1.by.css("div[id$=cabin-content] li"));
        this.flightQualityFilter = protractor_1.element.all(protractor_1.by.css("div[id$=quality-section-content] li"));
        this.cabinTitle = protractor_1.element(protractor_1.by.css("div[id$=cabin-title]"));
        this.flightQualityTitle = protractor_1.element(protractor_1.by.css("div[id$=quality-section-title]"));
        this.bookingProvidersTitle = protractor_1.element(protractor_1.by.css("div[id$=providers-title]"));
        this.stopsResetLink = protractor_1.element(protractor_1.by.css("a[id$=stops-reset]"));
        this.cabinResetLink = protractor_1.element(protractor_1.by.css("a[id$=cabin-reset]"));
        this.airlinesResetLink = protractor_1.element(protractor_1.by.css("a[id$=airlines-reset]"));
        this.airportsResetLink = protractor_1.element(protractor_1.by.css("a[id$=airports-section-reset]"));
        this.bookingProvidersResetLink = protractor_1.element(protractor_1.by.css("a[id$=providers-reset]"));
        this.flightResults = protractor_1.element.all(protractor_1.by.css(".Flights-Results-FlightResultItem"));
        this.popupDialog = protractor_1.element(protractor_1.by.css(".flightsDriveBy"));
        this.popupDialogCloseButton = this.popupDialog.element(protractor_1.by.css(".Button-No-Standard-Style.close"));
        this.jetBlueAirlinePrice = protractor_1.element(protractor_1.by.css["button[id$=B6-price]"]);
        this.jetBlueAirlineCheckBox = protractor_1.element(protractor_1.by.css["input[id$=B6-check]"]);
        this.oneStopCheckIcon = protractor_1.element(protractor_1.by.css("div[id$='-1-check-icon']"));
        this.oneStopCheckBox = protractor_1.element(protractor_1.by.css("input[id$='1-check']"));
        this.departureAndReturnSameCheckIcon = protractor_1.element(protractor_1.by.css("div[id$='sameair-check-icon']"));
        this.departureAndReturnSameCheckbox = protractor_1.element(protractor_1.by.css("input[id$=sameair-check]"));
        this.ewrCheckIcon = protractor_1.element(protractor_1.by.css("div[id$=EWR-check-icon]"));
        this.ewrCheckBox = protractor_1.element(protractor_1.by.css("input[id$=sameair-check]"));
        this.economyCabinCheckIcon = protractor_1.element(protractor_1.by.css("div[id$=e-check-icon]"));
        this.economoyCabinCheckBox = protractor_1.element(protractor_1.by.css("input[id$=e-check]"));
        this.longFlightsCheckIcon = protractor_1.element(protractor_1.by.css("div[id$='baditin-check-icon']"));
        this.longFlightCheckBox = protractor_1.element(protractor_1.by.css("input[id$='baditin-check']"));
        this.nonStopFilter = protractor_1.element(protractor_1.by.css("li[id$='-0']"));
        this.nonStopOnlyLink = protractor_1.element(protractor_1.by.css("button[id$='0-only']"));
        this.nonStopCheckBox = protractor_1.element(protractor_1.by.css("input[id$='0-check']"));
        this.alaskaAirlineFilter = protractor_1.element(protractor_1.by.css("li[id$='-0']"));
        this.alaskaAirlineOnlyLink = protractor_1.element(protractor_1.by.css("button[id$='-AS-only']"));
        this.alaskaAirlineCheckBox = protractor_1.element(protractor_1.by.css("input[id$='AS-check']"));
        this.cheapoairBookingProviderPrice = protractor_1.element(protractor_1.by.css("button[id$=-CHEAPOAIR-price]"));
        this.cheapoairBookingProviderCheckbox = protractor_1.element(protractor_1.by.css("input[id$=CHEAPOAIR-check]"));
    }
    get() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.get(this.kayakUrl);
        });
    }
    nonAngularApplication() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.ignoreSynchronization = yield true;
        });
    }
    closePopupDialog() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.popupDialog);
            yield this.popupDialogCloseButton.click();
        });
    }
    getTotalFlights() {
        return __awaiter(this, void 0, void 0, function* () {
            let flightsTotalCount = yield this.flightsTotalCount.getText();
            return Number(flightsTotalCount);
        });
    }
    getCheapestPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.cheapestPriceTab);
            return this.helper.getPrice(yield this.cheapestPriceTab.getText());
        });
    }
    getFlightsCount() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.flightCount);
            return this.flightCount.getText();
        });
    }
    oneStopChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.oneStopCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    clickOneStopCheckbox() {
        return __awaiter(this, void 0, void 0, function* () {
            let oneStopChecked = yield this.oneStopChecked();
            if (!oneStopChecked) {
                this.oneStopCheckIcon.click();
            }
        });
    }
    sameDepartureAndReturnAirportChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.departureAndReturnSameCheckbox.getAttribute("aria-checked")) === "true";
        });
    }
    checkSameDepartureAndReturnAirport() {
        return __awaiter(this, void 0, void 0, function* () {
            let sameDepartureAndReturnChecked = yield this.sameDepartureAndReturnAirportChecked();
            if (!sameDepartureAndReturnChecked) {
                yield this.departureAndReturnSameCheckIcon.click();
            }
        });
    }
    uncheckSameDepartureAndReturnAirport() {
        return __awaiter(this, void 0, void 0, function* () {
            let sameDepartureAndReturnChecked = yield this.sameDepartureAndReturnAirportChecked();
            if (sameDepartureAndReturnChecked) {
                yield this.departureAndReturnSameCheckIcon.click();
            }
        });
    }
    ewrAirportChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.ewrCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    checkEwrAirport() {
        return __awaiter(this, void 0, void 0, function* () {
            let ewrAirportChecked = yield this.ewrAirportChecked();
            if (!ewrAirportChecked) {
                yield this.ewrCheckIcon.click();
            }
        });
    }
    clickBookingProviderResetLink() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.bookingProvidersResetLink.click();
        });
    }
    bookingProviderResetLinkDisplayed() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.bookingProvidersResetLink.isDisplayed();
        });
    }
    clickTopFlightsLink() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.flightCountLink.click();
        });
    }
    clickResetCabinLink() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.cabinResetLink.click();
        });
    }
    resetCabinLinkDisplayed() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.cabinResetLink.isDisplayed();
        });
    }
    clickCabinTitle() {
        return __awaiter(this, void 0, void 0, function* () {
            let cabinExpand = yield this.flightQualityTitle.getAttribute("aria-expanded");
            if (cabinExpand === "false") {
                yield this.cabinTitle.click();
            }
        });
    }
    clickFlightQualityTitle() {
        return __awaiter(this, void 0, void 0, function* () {
            let flightQualityExpand = yield this.flightQualityTitle.getAttribute("aria-expanded");
            if (flightQualityExpand === "false") {
                yield this.flightQualityTitle.click();
            }
        });
    }
    clickBookingSitesTitle() {
        return __awaiter(this, void 0, void 0, function* () {
            let bookingExpand = yield this.bookingProvidersTitle.getAttribute("aria-expanded");
            if (bookingExpand === "false") {
                yield this.bookingProvidersTitle.click();
            }
        });
    }
    clickJetBluePrice() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.jetBlueAirlinePrice.click();
        });
    }
    jetBlueAirlineChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.jetBlueAirlineCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    longFlightsFilterChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.longFlightCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    checkLongFlightsFilter() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.clickFlightQualityTitle();
            let longFlightsFilterChecked = yield this.longFlightsFilterChecked();
            if (!longFlightsFilterChecked) {
                this.longFlightCheckBox.click();
            }
        });
    }
    stopResetLinkDisplayed() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.stopsResetLink);
            return this.stopsResetLink.isDisplayed();
        });
    }
    hoverAndClickNonStopOnlyLink() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.actions().mouseMove(this.nonStopFilter).perform();
            yield this.kayakCommonPage.waitUntillElementAppears(this.nonStopOnlyLink);
            yield this.nonStopOnlyLink.click();
        });
    }
    nonStopChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.nonStopCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    economyCabinChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.economoyCabinCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    uncheckEconomyCabin() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.clickCabinTitle();
            let economyCabinChecked = yield this.economyCabinChecked();
            if (economyCabinChecked) {
                this.economoyCabinCheckBox.click();
            }
        });
    }
    selectAlaskaAirlines() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.actions().mouseMove(this.alaskaAirlineFilter).perform();
            yield this.kayakCommonPage.waitUntillElementAppears(this.alaskaAirlineOnlyLink);
            yield this.alaskaAirlineOnlyLink.click();
        });
    }
    alaskaAirlinesFilterChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.alaskaAirlineCheckBox.getAttribute("aria-checked")) === "true";
        });
    }
    farePredictionPriceDisplayed() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.wait(this.kayakCommonPage.patternToBePresentInElement(this.flightPredictionGraph, /\w\w+/i));
            return this.flightPredictionGraph.isDisplayed();
        });
    }
    getTargetedArrayFromResults(selector) {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 30000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    let elementTextContents = yield [];
                    for (let result of results) {
                        let elementTextContent = yield result.element(protractor_1.by.css(selector)).getText();
                        elementTextContents.push(elementTextContent.trim());
                    }
                    return elementTextContents;
                });
            });
        });
    }
    resultsContainNonStopOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            let stops = yield this.getTargetedArrayFromResults(".section.stops");
            return (stops.indexOf("nonstop") === -1) ? false : true;
        });
    }
    resultsContainNonStopAndOneStopOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            let stops = yield this.getTargetedArrayFromResults(".section.stops");
            return ((stops.indexOf("nonstop") === -1) && (stops.indexOf("1 stop") === -1)) ? false : true;
        });
    }
    resultsContainJetBlueAirwaysOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            let airlines = yield this.getTargetedArrayFromResults(".section.times .bottom");
            return airlines.indexOf("JetBlue") ? false : true;
        });
    }
    resultsNotContainEWRAirport() {
        return __awaiter(this, void 0, void 0, function* () {
            let departureAiports = yield this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span");
            return departureAiports.indexOf("EWR") !== -1 ? false : true;
        });
    }
    resultsContainDepartureAndReturnSame() {
        return __awaiter(this, void 0, void 0, function* () {
            let departures = yield this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span:nth-child(3)");
            let returns = yield this.getTargetedArrayFromResults("div[id$=leg-1] .section.duration .bottom span:nth-child(1)");
            for (let departure in departures) {
                if (returns.indexOf(departure) === -1) {
                    return false;
                }
            }
            return true;
        });
    }
    resultsContainDepartureAndReturnSameAndDifferent() {
        return __awaiter(this, void 0, void 0, function* () {
            let departures = yield this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span:nth-child(3)");
            let returns = yield this.getTargetedArrayFromResults("div[id$=leg-1] .section.duration .bottom span:nth-child(1)");
            for (let departure in departures) {
                if (returns.indexOf(departure) === -1) {
                    return true;
                }
            }
            return false;
        });
    }
    resultsContainsAlaskaAirlinesOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            let airlines = yield this.getTargetedArrayFromResults(".providerName");
            return airlines.indexOf("Alaska Airlines") === -1 ? false : true;
        });
    }
    resultsContainsAllProviders() {
        return __awaiter(this, void 0, void 0, function* () {
            let airlines = yield this.getTargetedArrayFromResults(".providerName");
            return (airlines.indexOf("American Airlines") === -1) ? false : true;
        });
    }
    resultsNotContainEconomyCabins() {
        return __awaiter(this, void 0, void 0, function* () {
            let cabins = yield this.getTargetedArrayFromResults("span[id$=toolTipTarget]");
            return (cabins.indexOf("Economy") !== -1) ? false : true;
        });
    }
    resultsContainAllCabins() {
        return __awaiter(this, void 0, void 0, function* () {
            let cabins = yield this.getTargetedArrayFromResults("span[id$=toolTipTarget]");
            return (cabins.indexOf("Economy") === -1 && cabins.indexOf("Saver") === -1 && cabins.indexOf("Main") === -1)
                ? false : true;
        });
    }
    resetAllFilters() {
        return __awaiter(this, void 0, void 0, function* () {
            let stopsResetLinkDisplayed = yield this.stopsResetLink.isDisplayed();
            let cabinResetLinkDisplayed = yield this.cabinResetLink.isDisplayed();
            let airlinesResetLinkDisplayed = yield this.airlinesResetLink.isDisplayed();
            let airportsResetLinkDisplayed = yield this.airportsResetLink.isDisplayed();
            let bookingProvidersResetLinkDisplayed = yield this.bookingProvidersResetLink.isDisplayed();
            if (!stopsResetLinkDisplayed && !cabinResetLinkDisplayed && !airlinesResetLinkDisplayed && !airportsResetLinkDisplayed && !bookingProvidersResetLinkDisplayed) {
                return true;
            }
            else {
                return false;
            }
        });
    }
    getCheapoAirBookingProviderPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            let price = yield this.cheapoairBookingProviderPrice.getText();
            return Number(price.split("$")[1]);
        });
    }
    cheapoAirBookingProviderChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return (yield this.cheapoairBookingProviderCheckbox.getAttribute("aria-checked")) === "true";
        });
    }
    clickCheapoAirBookingProviderPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.cheapoairBookingProviderPrice.click();
        });
    }
    airportStopsCheck(selector, attribute = null) {
        return __awaiter(this, void 0, void 0, function* () {
            return this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        yield protractor_1.browser.actions().mouseMove(stop).mouseMove(stop).perform();
                        let stopChecked = (yield (attribute)) ? stop.element(protractor_1.by.css(selector)).getAttribute(attribute) : stop.element(protractor_1.by.css(selector)).getText();
                        if (!stopChecked || stopChecked === "false") {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    airportStopFiltersChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.airportStopsCheck("input", "aria-checked");
        });
    }
    airportStopFiltersContainPrices() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.airportStopsCheck(".price");
        });
    }
    airportStopFiltersHighlightedAndAppearOnlyOnHover() {
        return __awaiter(this, void 0, void 0, function* () {
            let that = yield this;
            return this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        yield protractor_1.browser.actions().mouseMove(stop).mouseMove(stop).perform();
                        yield protractor_1.browser.wait(that.expectedCondition.visibilityOf(stop.element(protractor_1.by.css("button[id$='-only']"))), 30000);
                        let onlyLink = yield stop.element(protractor_1.by.css("button[id$='-only']")).isPresent();
                        let highlightedColor = yield stop.getCssValue("background-color");
                        if (!onlyLink && highlightedColor !== "rgba(219, 238, 255, 1)") {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
}
exports.FlightResultsPage = FlightResultsPage;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiRmxpZ2h0UmVzdWx0c1BhZ2UuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9GbGlnaHRSZXN1bHRzUGFnZS50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUEsMkNBQXlJO0FBQ3pJLDZDQUF3QztBQUN4QywrQ0FBNEM7QUFFNUM7SUFBQTtRQUVDLG9CQUFlLEdBQWUsSUFBSSx1QkFBVSxFQUFFLENBQUM7UUFDL0MsV0FBTSxHQUFnQixJQUFJLHlCQUFXLEVBQUUsQ0FBQztRQUN4QyxzQkFBaUIsR0FBaUMsdUJBQVUsQ0FBQyxrQkFBa0IsQ0FBQztRQUNoRixhQUFRLEdBQVcsNkRBQTZELENBQUM7UUFDakYsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHFCQUFxQixDQUFDLENBQUMsQ0FBQztRQUNyRSwwQkFBcUIsR0FBRyxvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMERBQTBELENBQUMsQ0FBQyxDQUFDO1FBQ3BHLHFCQUFnQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscUJBQXFCLENBQUMsQ0FBQyxDQUFDO1FBQ3pFLGdCQUFXLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsb0JBQWUsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLGdDQUFnQyxDQUFDLENBQUMsQ0FBQztRQUNuRixzQkFBaUIsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDZCQUE2QixDQUFDLENBQUMsQ0FBQztRQUNsRixnQkFBVyxHQUF1QixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDJCQUEyQixDQUFDLENBQUMsQ0FBQztRQUNuRixtQkFBYyxHQUF1QixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHVDQUF1QyxD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