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
const commonPage_1 = require("./commonPage");
const kayakHelper_1 = require("./kayakHelper");
class FlightResultsPage {
    constructor() {
        this.kayakCommonPage = new commonPage_1.commonPage();
        this.helper = new kayakHelper_1.kayakHelper();
        this.kayakUrl = "https://www.kayak.com/flights/NYC-LAX/2019-08-18/2019-08-25";
        this.flightPredictionGraph = protractor_1.element(protractor_1.by.css("div[class*='FlightQueryPricePrediction'] div[id$=advice]"));
        this.cheapestPrice = protractor_1.element(protractor_1.by.css("a[id$='price_aTab']"));
        this.flightCount = protractor_1.element(protractor_1.by.css("div[id$=resultsCount]"));
        this.flightCountLink = protractor_1.element(protractor_1.by.css("div[id$=resultsCount] .showAll"));
        this.flightsTotalCount = protractor_1.element(protractor_1.by.css("span[id$=counts-totalCount]"));
        this.stopsFilter = protractor_1.element.all(protractor_1.by.css("div[id$=stops-content] li"));
        this.airlinesFilter = protractor_1.element.all(protractor_1.by.css("div[id$=airlines-airlines-content] li"));
        this.bookingProvidersFilter = protractor_1.element.all(protractor_1.by.css("div[id$=providers-content] li"));
        this.cabinFilter = protractor_1.element.all(protractor_1.by.css("div[id$=cabin-content] li"));
        this.qualityFilter = protractor_1.element.all(protractor_1.by.css("div[id$=quality-section-content] li"));
        this.stopsInResults = protractor_1.element.all(protractor_1.by.css(".section.stops"));
        this.sameDepartAndReturnCheckbox = protractor_1.element(protractor_1.by.css("div[id$=sameair-check-icon]"));
        this.EWRCheckbox = protractor_1.element(protractor_1.by.css("div[id$=EWR-check-icon]"));
        this.cabinTitle = protractor_1.element(protractor_1.by.css("div[id$=cabin-title]"));
        this.flightQualityTitle = protractor_1.element(protractor_1.by.css("div[id$=quality-section-title]"));
        this.bookingProvidersTitle = protractor_1.element(protractor_1.by.css("div[id$=providers-title]"));
        this.stopsResetLink = protractor_1.element(protractor_1.by.css("a[id$=stops-reset]"));
        this.cabinResetLink = protractor_1.element(protractor_1.by.css("a[id$=cabin-reset]"));
        this.bookingProvidersResetLink = protractor_1.element(protractor_1.by.css("a[id$=providers-reset]"));
        this.flightResults = protractor_1.element.all(protractor_1.by.css(".Flights-Results-FlightResultItem"));
        this.popupDialog = protractor_1.element(protractor_1.by.css(".flightsDriveBy"));
        this.popupDialogCloseButton = this.popupDialog.element(protractor_1.by.css(".Button-No-Standard-Style.close"));
    }
    get() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.get(this.kayakUrl);
        });
    }
    isNonAngularApplication() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.ignoreSynchronization = yield true;
        });
    }
    maximizeBrowser() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.manage().window().setSize(1600, 1000);
        });
    }
    closePopup() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.popupDialog);
            yield this.popupDialogCloseButton.click();
        });
    }
    getTotalFlights() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.flightsTotalCount.getText().then(function (totalFlights) {
                return Number(totalFlights);
            });
        });
    }
    getCheapestPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.cheapestPrice);
            return this.helper.getPrice(yield this.cheapestPrice.getText());
        });
    }
    getFlightsCount() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.flightCount);
            return this.flightCount.getText();
        });
    }
    getBookingProviderFilterPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.bookingProvidersFilter.then(function (providers) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let provider of providers) {
                        yield protractor_1.browser.actions().mouseMove(provider).perform();
                        yield protractor_1.browser.sleep(1000);
                        let PriceText = yield provider.element(protractor_1.by.css("button[id$=-price]")).getText();
                        if (PriceText.trim()) {
                            return yield this.helper.getPrice(PriceText);
                        }
                    }
                    yield protractor_1.browser.sleep(3000);
                });
            });
        });
    }
    clickOneStopCheckbox() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.stopsFilter.then(function (stops) {
                stops[1].element(protractor_1.by.css("div[id$=check-icon]")).click();
            });
        });
    }
    checkSameDepartAndReturn() {
        return __awaiter(this, void 0, void 0, function* () {
            let isSameDepartAndReturnChecked = yield this.sameDepartAndReturnCheckbox.getAttribute("aria-checked");
            if (isSameDepartAndReturnChecked === "false") {
                yield this.sameDepartAndReturnCheckbox.click();
            }
        });
    }
    unCheckSameDepartAndReturn() {
        return __awaiter(this, void 0, void 0, function* () {
            let isSameDepartAndReturnChecked = yield this.sameDepartAndReturnCheckbox.getAttribute("aria-checked");
            if (isSameDepartAndReturnChecked === "true") {
                yield this.sameDepartAndReturnCheckbox.click();
            }
        });
    }
    clickEWRCheckbox() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.EWRCheckbox.click();
        });
    }
    clickBookingProviderResetLink() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.bookingProvidersResetLink.click();
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
            yield protractor_1.browser.sleep(3000);
            return this.airlinesFilter.then(function (airlines) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let airline of airlines) {
                        let airlineText = yield airline.element(protractor_1.by.css("label[id$=check-label]")).getText();
                        airlineText = airlineText.trim();
                        if (airlineText.indexOf("JetBlue") !== -1) {
                            yield airline.element(protractor_1.by.css("button[id$=-price")).click();
                        }
                    }
                    yield protractor_1.browser.sleep(3000);
                });
            });
        });
    }
    clickLongFlightsFilter() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.qualityFilter.then(function (flights) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let flight of flights) {
                        let flightText = yield flight.element(protractor_1.by.css("label[id$=check-label]")).getText();
                        flightText = flightText.trim();
                        if (flightText.indexOf("longer flights") !== -1) {
                            yield flight.element(protractor_1.by.css("div[id$=check-icon]")).click();
                        }
                    }
                    yield protractor_1.browser.sleep(5000);
                });
            });
        });
    }
    isStopFiltersChecked() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        const stopChecked = yield stop.element(protractor_1.by.tagName("input")).getAttribute("aria-checked");
                        if (stopChecked === "false") {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isStopFiltersContainPrices() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        const price = yield stop.element(protractor_1.by.className("price")).getText();
                        if (price.match(/\$((?:\d|\,)*\.?\d+)/g) === null) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isStopFiltersHighlightedAndShowOnlyOnHover() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        yield protractor_1.browser.actions().mouseMove(stop).perform();
                        yield protractor_1.browser.sleep(1000);
                        const onlyLink = yield stop.element(protractor_1.by.css("button[id$='-only']")).isPresent();
                        if (!onlyLink) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResetLinkAppeared() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.kayakCommonPage.waitUntillElementAppears(this.stopsResetLink);
            return this.stopsResetLink.isDisplayed();
        });
    }
    hoverAndClickNonStopOnlyLink() {
        return __awaiter(this, void 0, void 0, function* () {
            this.stopsFilter.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        yield protractor_1.browser.actions().mouseMove(stop).perform();
                        yield protractor_1.browser.sleep(1000);
                        let stopText = yield stop.element(protractor_1.by.css("label[id$=check-label]")).getText();
                        if (stopText.trim() === "Nonstop") {
                            yield stop.element(protractor_1.by.css("button[id$='-only']")).click();
                        }
                    }
                    yield protractor_1.browser.sleep(5000);
                });
            });
        });
    }
    uncheckEconomyFilter() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.cabinFilter.then(function (cabins) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let cabin of cabins) {
                        let cabinText = yield cabin.element(protractor_1.by.css("label[id$=check-label]")).getText();
                        if (cabinText.trim().indexOf("Economy") !== -1) {
                            yield cabin.element(protractor_1.by.css("div[id$=check-icon]")).click();
                        }
                    }
                    yield protractor_1.browser.sleep(5000);
                });
            });
        });
    }
    selectAlaskaAirlines() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.bookingProvidersFilter.then(function (providers) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let provider of providers) {
                        yield protractor_1.browser.actions().mouseMove(provider).perform();
                        yield protractor_1.browser.sleep(3000);
                        let providerText = yield provider.element(protractor_1.by.css("label[id$=check-label]")).getText();
                        if (providerText.trim().indexOf("Alaska Airlines") !== -1) {
                            yield provider.element(protractor_1.by.css("button[id$=-only")).click();
                            return;
                        }
                    }
                    yield protractor_1.browser.sleep(5000);
                });
            });
        });
    }
    isPredictionPriceDisplayed() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.wait(this.kayakCommonPage.patternToBePresentInElement(this.flightPredictionGraph, /buy now/i));
            if (this.flightPredictionGraph.isDisplayed()) {
                return true;
            }
        });
    }
    isResultsContainNonStopOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return yield this.stopsInResults.then(function (stops) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let stop of stops) {
                        let stopText = yield stop.getText();
                        if (stopText.indexOf("nonstop") === -1) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainNonStopAndOneStopOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(2000);
            return this.stopsInResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let stopText = yield result.getText();
                        if ((stopText.trim().indexOf("nonstop") === -1) && (stopText.indexOf("1 stop") === -1)) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainJetBlueAirwaysOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(5000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let airline = yield result.element(protractor_1.by.css(".section.times .bottom")).getText();
                        if (airline.trim().indexOf("JetBlue") === -1) {
                            console.log(airline);
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsNotContainEWRAirport() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let departed = yield result.element(protractor_1.by.css("div[id$=leg-0")).element(protractor_1.by.css(".section.duration .bottom")).getText();
                        departed = departed.split("‐")[0].trim();
                        if (departed.indexOf("EWR") !== -1) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainDepartAndReturnSame() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let departed = yield result.element(protractor_1.by.css("div[id$=leg-0")).element(protractor_1.by.css(".section.duration .bottom")).getText();
                        let returned = yield result.element(protractor_1.by.css("div[id$=leg-1")).element(protractor_1.by.css(".section.duration .bottom")).getText();
                        departed = yield departed.split("‐")[1].trim();
                        returned = yield returned.split("‐")[0].trim();
                        if (returned.indexOf(departed) === -1) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainDepartAndReturnSameAndDifferent() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(3000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let departed = yield result.element(protractor_1.by.css("div[id$=leg-0")).element(protractor_1.by.css(".section.duration .bottom")).getText();
                        let returned = yield result.element(protractor_1.by.css("div[id$=leg-1")).element(protractor_1.by.css(".section.duration .bottom")).getText();
                        departed = yield departed.split("‐")[1].trim();
                        returned = yield returned.split("‐")[0].trim();
                        if (returned.indexOf(departed) === -1) {
                            return true;
                        }
                    }
                    return false;
                });
            });
        });
    }
    isResultsContainsAlaskaAirlinesOnly() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(7000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let airline = yield result.element(protractor_1.by.css(".providerName")).getText();
                        airline = yield airline.trim();
                        if (airline.indexOf("Alaska Airlines") === -1) {
                            return false;
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainNotEconomyCabins() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(8000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let cabinExists = yield result.element(protractor_1.by.css("span[id$=toolTipTarget]")).isPresent();
                        if (cabinExists) {
                            let cabin = yield result.element(protractor_1.by.css("span[id$=toolTipTarget]")).getText();
                            if (cabin.trim().indexOf("Economy") !== -1) {
                                return false;
                            }
                        }
                    }
                    return true;
                });
            });
        });
    }
    isResultsContainAllCabins() {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.sleep(8000);
            return this.flightResults.then(function (results) {
                return __awaiter(this, void 0, void 0, function* () {
                    for (let result of results) {
                        let cabinExists = yield result.element(protractor_1.by.css("span[id$=toolTipTarget]")).isPresent();
                        if (cabinExists) {
                            let cabin = yield result.element(protractor_1.by.css("span[id$=toolTipTarget]")).getText();
                            if (cabin.trim().indexOf("Economy") === -1) {
                                return true;
                            }
                        }
                    }
                    return false;
                });
            });
        });
    }
}
exports.FlightResultsPage = FlightResultsPage;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZmxpZ2h0UmVzdWx0c1BhZ2UuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9mbGlnaHRSZXN1bHRzUGFnZS50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUEsMkNBQTJHO0FBQzNHLDZDQUF1QztBQUN2QywrQ0FBNEM7QUFFNUM7SUFBQTtRQUVDLG9CQUFlLEdBQUcsSUFBSSx1QkFBVSxFQUFFLENBQUM7UUFDbkMsV0FBTSxHQUFHLElBQUkseUJBQVcsRUFBRSxDQUFDO1FBRTNCLGFBQVEsR0FBRyw2REFBNkQsQ0FBQztRQUN6RSwwQkFBcUIsR0FBRyxvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMERBQTBELENBQUMsQ0FBQyxDQUFDO1FBQ3BHLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsZ0JBQVcsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHVCQUF1QixDQUFDLENBQUMsQ0FBQztRQUN0RSxvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsZ0NBQWdDLENBQUMsQ0FBQyxDQUFDO1FBQ25GLHNCQUFpQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsNkJBQTZCLENBQUMsQ0FBQyxDQUFDO1FBQ2xGLGdCQUFXLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMkJBQTJCLENBQUMsQ0FBQyxDQUFDO1FBQ25GLG1CQUFjLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsdUNBQXVDLENBQUMsQ0FBQyxDQUFDO1FBQ2xHLDJCQUFzQixHQUF1QixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLCtCQUErQixDQUFDLENBQUMsQ0FBQztRQUNsRyxnQkFBVyxHQUF1Qixv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