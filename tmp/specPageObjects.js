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
var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
const FlightResultsPage_1 = require("./FlightResultsPage");
describe('Flight Prediction Graph: ', function () {
    const flightResults = new FlightResultsPage_1.FlightResultsPage();
    const flightCountBefore = flightResults.getTotalFlights();
    before("Should open kayak site and close popup dialog", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.get();
            yield flightResults.closePopupDialog();
        });
    });
    it("Should FPP(Flight Prediction Price) graph Appears in Left Rail", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.farePredictionPriceDisplayed()).to.be.true;
        });
    });
    it("Should display xxx of XXXX flights on top", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.getFlightsCount()).to.match(/^[0-9]+ of [0-9]+ flights$/gm);
        });
    });
    it("Should check all airport stops", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.airportStopFiltersChecked()).to.be.true;
        });
    });
    it("Should display prices next to all stops", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.airportStopFiltersContainPrices()).to.be.true;
        });
    });
    it("Should hover cursor over each stop option and verify if line is highlighted in blue and a 'only' link appears", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.airportStopFiltersHighlightedAndAppearOnlyOnHover()).to.be.true;
        });
    });
    it("Should click nonstop 'only' link", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.hoverAndClickNonStopOnlyLink();
            expect(yield flightResults.nonStopChecked()).to.be.true;
        });
    });
    it("Should display results with nonstop only", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainNonStopOnly()).to.be.true;
        });
    });
    it("Should display reset link on the top of stop filters", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.stopResetLinkDisplayed()).to.be.true;
        });
    });
    it("Should click onestop checkbox", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickOneStopCheckbox();
            expect(yield flightResults.oneStopChecked()).to.be.true;
        });
    });
    it("Should display results with 1-stop and non-stop", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainNonStopAndOneStopOnly()).to.be.true;
        });
    });
    it("Should check 'Depart/Return Same' under Airports", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.checkSameDepartureAndReturnAirport();
            expect(yield flightResults.sameDepartureAndReturnAirportChecked()).to.be.true;
        });
    });
    it("Should display results with same departure and return airport", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainDepartureAndReturnSame()).to.be.true;
        });
    });
    it("should display fewer number of flight results", function () {
        return __awaiter(this, void 0, void 0, function* () {
            const flightCountAfter = yield flightResults.getTotalFlights();
            expect(flightCountBefore).to.eventually.be.most(flightCountAfter);
        });
    });
    it("Should uncheck 'Depart/Return Same' under airports", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.uncheckSameDepartureAndReturnAirport();
            expect(yield flightResults.sameDepartureAndReturnAirportChecked()).to.be.false;
        });
    });
    it("Should display results with different departure and arrival airports", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainDepartureAndReturnSameAndDifferent()).to.be.true;
        });
    });
    it("Should check EWR under Airports", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.checkEwrAirport();
            expect(yield flightResults.ewrAirportChecked()).to.be.true;
        });
    });
    it("Should display results without EWR airport", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsNotContainEWRAirport()).to.be.true;
        });
    });
    it("Should click Price for JetBlue Airways", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickJetBluePrice();
            expect(yield flightResults.jetBlueAirlineChecked()).to.be.true;
        });
    });
    it("Should display results with jetblue Airways only", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainJetBlueAirwaysOnly()).to.be.true;
        });
    });
    it("Should uncheck economy cabin under cabins", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.uncheckEconomyCabin();
            expect(yield flightResults.economyCabinChecked()).to.be.false;
        });
    });
    it("Should results do not include Economy cabin results", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsNotContainEconomyCabins()).to.be.true;
        });
    });
    it("Should click reset link above cabins", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickResetCabinLink();
            expect(yield flightResults.resetCabinLinkDisplayed()).to.be.false;
        });
    });
    it("Should display results with all cabin classes", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainAllCabins()).to.be.true;
        });
    });
    it("Should check 'Show xx longer flights' filter option", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.checkLongFlightsFilter();
            expect(flightResults.longFlightsFilterChecked()).to.be.true;
        });
    });
    it("Should display more number of results", function () {
        return __awaiter(this, void 0, void 0, function* () {
            const flightCountAfter = yield flightResults.getTotalFlights();
            expect(flightCountBefore).to.eventually.be.below(flightCountAfter);
        });
    });
    it("Should click Alaska Airlines 'only' link", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.selectAlaskaAirlines();
            expect(yield flightResults.alaskaAirlinesFilterChecked()).to.be.true;
        });
    });
    it("Should display results with Alaska Airlines only", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.true;
        });
    });
    it("Should click reset link", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickBookingProviderResetLink();
            expect(yield flightResults.bookingProviderResetLinkDisplayed()).to.be.false;
        });
    });
    it("Should display results with all booking providers", function () {
        return __awaiter(this, void 0, void 0, function* () {
            expect(yield flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.false;
        });
    });
    it("Should click CheapoAir provider price", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickCheapoAirBookingProviderPrice();
            expect(yield flightResults.cheapoairBookingProviderCheckbox).to.be.true;
        });
    });
    it("Should CheapoAir price matches cheapest result", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.selectAlaskaAirlines();
            expect(yield flightResults.getCheapestPrice()).to.be.equal(yield flightResults.getCheapoAirBookingProviderPrice());
        });
    });
    it("Should click xxx of XXXX on top and verify if all filters reset again", function () {
        return __awaiter(this, void 0, void 0, function* () {
            yield flightResults.clickTopFlightsLink();
            expect(yield flightResults.resetAllFilters()).to.be.false;
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic3BlY1BhZ2VPYmplY3RzLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3BlY1BhZ2VPYmplY3RzLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBQSxJQUFJLElBQUksR0FBRyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUM7QUFDM0IsSUFBSSxjQUFjLEdBQUcsT0FBTyxDQUFDLGtCQUFrQixDQUFDLENBQUM7QUFDakQsSUFBSSxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsQ0FBQztBQUN6QixJQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDO0FBQ3pCLDJEQUFxRDtBQUVyRCxRQUFRLENBQUMsMkJBQTJCLEVBQUU7SUFFckMsTUFBTSxhQUFhLEdBQUcsSUFBSSxxQ0FBaUIsRUFBRSxDQUFDO0lBQzlDLE1BQU0saUJBQWlCLEdBQUcsYUFBYSxDQUFDLGVBQWUsRUFBRSxDQUFDO0lBRTFELE1BQU0sQ0FBQywrQ0FBK0MsRUFBRTs7WUFFdkQsTUFBTSxhQUFhLENBQUMsR0FBRyxFQUFFLENBQUM7WUFDMUIsTUFBTSxhQUFhLENBQUMsZ0JBQWdCLEVBQUUsQ0FBQztRQUN4QyxDQUFDO0tBQUEsQ0FBQyxDQUFDO0lBRUgsRUFBRSxDQUFDLGdFQUFnRSxFQUFFOztZQUVwRSxNQUFNLENBQUMsTUFBTSxhQUFhLENBQUMsNEJBQTRCLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDO1FBQ3ZFLENBQUM7S0FBQSxDQUFDLENBQUM7SUFFSCxFQUFFLENBQUMsMkNBQTJDLEVBQUU7O1lBRS9DLE1BQU0sQ0FBQyxNQUFNLGFBQWEsQ0FBQyxlQUFlLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxLQUFLLENBQUMsOEJBQThCLENBQUMsQ0FBQztRQUN4RixDQUFDO0tBQUEsQ0FBQyxDQUFDO0lBRUgsRUFBRSxDQUFDLGdDQUFnQyxFQUFFOztZQUVwQyxNQUFNLENBQUMsTUFBTSxhQUFhLENBQUMs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