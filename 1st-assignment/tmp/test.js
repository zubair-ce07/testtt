"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const homePageObject_1 = require("./homePageObject");
const flightsPageObject_1 = require("./flightsPageObject");
const searchFormObject_1 = require("./searchFormObject");
var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
let homePageObject = new homePageObject_1.HomePageObject();
let flightsPageObject = new flightsPageObject_1.FlightsPageObject();
let searchFormObject = new searchFormObject_1.SearchFormObject();
describe("kayak Automation", function () {
    return __awaiter(this, void 0, void 0, function* () {
        before(function () {
            return __awaiter(this, void 0, void 0, function* () {
                protractor_1.browser.waitForAngularEnabled(false);
                yield protractor_1.browser.get('https://www.kayak.com');
            });
        });
        it("Select flights from top", function () {
            homePageObject.clickFlights().should.eventually.include('flights');
        });
        it("Should display the origin field", function () {
            searchFormObject.getDepartureDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the destination field", function () {
            searchFormObject.getDestinationDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the departure date field", function () {
            searchFormObject.departureDateFieldDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the return date field", function () {
            searchFormObject.returnDateFieldDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display ‘Round-trip’ in trip type field", function () {
            homePageObject.roundTripField.getText().should.eventually.be.equal('Round-trip');
        });
        it("Switch to ‘One-way’ trip type mode", function () {
            homePageObject.changeToOneWayTrip();
            homePageObject.roundTripField.getText().should.eventually.be.equal('One-way');
        });
        it("Switch to ‘Multi-city’ trip type mode", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.changeToMulticityTrip();
                yield homePageObject.roundTripField.getText().should.eventually.be.equal('Multi-city');
            });
        });
        it("Change number of ‘adults’ from travelers field to 9", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.addAdultPassengers(10);
                yield homePageObject.getAdultsLimitMessage().should.eventually.be.equal("Searches cannot have more than 9 adults");
            });
        });
        it("Switch to ‘Round-trip’ trip type mode", function () {
            homePageObject.changeToRoundTrip();
            homePageObject.roundTripField.getText().should.eventually.be.equal('Round-trip');
        });
        it("Should display ‘Paris (PAR)’ in origin field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.setDeparture("PAR");
                homePageObject.getDepartureValue().should.eventually.be.equal("Paris (PAR)");
            });
        });
        it("Should display ‘New York (NYC)’ in the destination field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.setDestination("NYC");
                homePageObject.getDestinationValue().should.eventually.be.equal("New York (NYC)");
            });
        });
        it("Should display accurate date in departure field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.fillDatesDeparture();
                homePageObject.getDepartureDate().getText().should.eventually.be.equal(homePageObject.getTripDates(3));
            });
        });
        it("Should display accurate date in return date field", function () {
            homePageObject.fillDatesReturn();
            homePageObject.getReturnDate().should.eventually.be.equal(homePageObject.getTripDates(6));
        });
        it("Should display all unchecked checkboxes in compare-to block", function () {
            homePageObject.uncheckAllCheckBox();
        });
        it("Should display ‘4 Travelers’ in the travelers field", function () {
            homePageObject.decreaseAdultPassengers(6);
            homePageObject.getAdultPassenger().should.eventually.be.equal('4');
        });
        it("Should display ‘6 Travelers’ in the travelers field", function () {
            homePageObject.addChildPassengers(2);
            homePageObject.getChildPassenger().should.eventually.be.equal('2');
        });
        it("Should display correct filled-in search form on results page", function () {
            homePageObject.clickSearch().should.eventually.include('sort=bestflight_a');
        });
        it("Should display the origin field", function () {
            searchFormObject.getDepartureDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the destination field", function () {
            searchFormObject.getDestinationDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the departure date field", function () {
            searchFormObject.departureDateFieldDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display the return date field", function () {
            searchFormObject.returnDateFieldDisplay().isDisplayed().should.eventually.be.true;
        });
        it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const cheapPrice = flightsPageObject.getCheapestPrice();
                const bestPrice = flightsPageObject.getBestPrice();
                const quickPrice = flightsPageObject.getQuickestPrice();
                yield protractor_1.promise.all([cheapPrice, bestPrice, quickPrice]);
            });
        });
        it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", function () {
            const cheapTime = flightsPageObject.getCheapestTime();
            const bestTime = flightsPageObject.getBestTime();
            const quickTime = flightsPageObject.getQuickestTime();
            protractor_1.promise.all([cheapTime, bestTime, quickTime]);
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3Rlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBMEQ7QUFDMUQscURBQWtEO0FBQ2xELDJEQUF3RDtBQUN4RCx5REFBc0Q7QUFHdEQsSUFBSSxJQUFJLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDO0FBQzNCLElBQUksY0FBYyxHQUFHLE9BQU8sQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO0FBQ2pELElBQUksQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLENBQUM7QUFDekIsSUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQztBQUN6QixJQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7QUFDM0IsSUFBSSxjQUFjLEdBQW1CLElBQUksK0JBQWMsRUFBRSxDQUFDO0FBQzFELElBQUksaUJBQWlCLEdBQXNCLElBQUkscUNBQWlCLEVBQUUsQ0FBQztBQUNuRSxJQUFJLGdCQUFnQixHQUFxQixJQUFJLG1DQUFnQixFQUFFLENBQUM7QUFFaEUsUUFBUSxDQUFDLGtCQUFrQixFQUFFOztRQUMzQixNQUFNLENBQUM7O2dCQUNMLG9CQUFPLENBQUMscUJBQXFCLENBQUMsS0FBSyxDQUFDLENBQUM7Z0JBQ3JDLE1BQU0sb0JBQU8sQ0FBQyxHQUFHLENBQUMsdUJBQXVCLENBQUMsQ0FBQztZQUM3QyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHlCQUF5QixFQUFFO1lBQzVCLGNBQWMsQ0FBQyxZQUFZLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLE9BQU8sQ0FBQyxTQUFTLENBQUMsQ0FBQTtRQUNwRSxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxpQ0FBaUMsRUFBRTtZQUNwQyxnQkFBZ0IsQ0FBQyxtQkFBbUIsRUFBRSxDQUFDLFdBQVcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMs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