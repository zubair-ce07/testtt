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
var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
let homePageObject = new homePageObject_1.HomePageObject();
let flightsPageObject = new flightsPageObject_1.FlightsPageObject();
describe("kayak Automation", function () {
    before(function () {
        protractor_1.browser.waitForAngularEnabled(false);
        protractor_1.browser.get('https://www.kayak.com');
    });
    it("Select flights from top", function () {
        expect(homePageObject.clickFlights());
    });
    it("Should display the origin field", function () {
        expect(homePageObject.getOrigin()).to.eventually.be.true;
    });
    it("Should display the destination field", function () {
        expect(homePageObject.getDestination()).to.eventually.be.true;
    });
    it("Should display the departure date field", function () {
        expect(homePageObject.departureField()).to.eventually.be.true;
    });
    it("Should display the return date field", function () {
        expect(homePageObject.returnField()).to.eventually.be.true;
    });
    it("Should display ‘Round-trip’ in trip type field", function () {
        expect(homePageObject.roundTripTypeField()).to.eventually.be.equal('true');
    });
    it("Switch to ‘One-way’ trip type mode", function () {
        homePageObject.clickSwitch();
        homePageObject.clickOneWay();
        expect(homePageObject.departureField()).to.eventually.be.true;
    });
    it("Switch to ‘Multi-city’ trip type mode", function () {
        homePageObject.clickSwitch();
        homePageObject.clickMultiCity();
        expect(homePageObject.multiCities()).to.eventually.be.true;
    });
    it("Switch to ‘Round-trip’ trip type mode", function () {
        homePageObject.clickSwitch();
        homePageObject.clickRoundTrip();
        expect(homePageObject.returnField()).to.eventually.be.true;
    });
    it("Change number of ‘adults’ from travelers field to 9", function () {
        homePageObject.clickTravelersGrid();
        homePageObject.addAdultPassengers(10);
        expect(homePageObject.getAdultsLimitMessage()).to.eventually.be.equal("Searches cannot have more than 9 adults");
    });
    it("Should display ‘Paris (PAR)’ in origin field", function () {
        homePageObject.clickSwitch();
        homePageObject.clickRoundTrip();
        homePageObject.clickOriginField();
        homePageObject.fillOrigin("PAR");
        homePageObject.selectOrigin();
        expect(homePageObject.getOriginValue()).to.eventually.be.include("Paris (PAR)");
    });
    it("Should display ‘New York (NYC)’ in the destination field", function () {
        homePageObject.clickDestinationField();
        homePageObject.fillDestination("NYC");
        homePageObject.selectDestination();
        expect(homePageObject.getDestinationValue()).to.eventually.be.include("New York (NYC)");
    });
    it("Should display ‘4 Travelers’ in the travelers field", function () {
        homePageObject.clickPassengersDropdown();
        homePageObject.decreaseAdultPassengers(6);
        expect(homePageObject.getAdultPassenger()).to.eventually.be.equal('4');
    });
    it("Should display ‘6 Travelers’ in the travelers field", function () {
        homePageObject.addChildPassengers(2);
        expect(homePageObject.getChildPassenger()).to.eventually.be.equal('2');
    });
    it("Should display accurate date in departure field", function () {
        homePageObject.clickDepartureField();
        homePageObject.fillDatesDeparture();
        expect(homePageObject.getDepartureDate()).to.eventually.equal(homePageObject.getTripDates(3));
    });
    it("Should display accurate date in return date field", function () {
        homePageObject.fillDatesReturn();
        expect(homePageObject.getReturnDate()).to.eventually.equal(homePageObject.getTripDates(6));
    });
    it("Should display all unchecked checkboxes in compare-to block", function () {
        homePageObject.clickSwitch();
        homePageObject.clickRoundTrip();
        expect(homePageObject.uncheckAllCheckBox());
    });
    it("Should display correct filled-in search form on results page", function () {
        homePageObject.clickSearch();
        homePageObject.switchTabs();
        protractor_1.browser.sleep(5000);
        expect(flightsPageObject.getDeparture()).to.eventually.equal("Paris (PAR)");
        expect(flightsPageObject.getDestination()).to.eventually.equal("New York (NYC)");
        expect(flightsPageObject.getDepartureDate()).to.eventually.equal(flightsPageObject.getTripDates(3));
        expect(flightsPageObject.getReturnDate()).to.eventually.equal(flightsPageObject.getTripDates(6));
    });
    it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", function () {
        return __awaiter(this, void 0, void 0, function* () {
            const cheapPrice = yield flightsPageObject.getCheapestPrice();
            const bestPrice = yield flightsPageObject.getBestPrice();
            const quickPrice = yield flightsPageObject.getQuickestPrice();
            expect(cheapPrice).to.be.at.most(bestPrice);
            expect(cheapPrice).to.be.at.most(quickPrice);
        });
    });
    it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", function () {
        return __awaiter(this, void 0, void 0, function* () {
            const cheapTime = yield flightsPageObject.getCheapestTime();
            const bestTime = yield flightsPageObject.getBestTime();
            const quickTime = yield flightsPageObject.getQuickestTime();
            expect(quickTime).to.be.at.most(cheapTime);
            expect(quickTime).to.be.at.most(bestTime);
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3Rlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBMEQ7QUFDMUQscURBQWtEO0FBQ2xELDJEQUF3RDtBQUV4RCxJQUFJLElBQUksR0FBRyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUM7QUFDM0IsSUFBSSxjQUFjLEdBQUcsT0FBTyxDQUFDLGtCQUFrQixDQUFDLENBQUM7QUFDakQsSUFBSSxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsQ0FBQztBQUN6QixJQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDO0FBQ3pCLElBQUksY0FBYyxHQUFtQixJQUFJLCtCQUFjLEVBQUUsQ0FBQztBQUMxRCxJQUFJLGlCQUFpQixHQUFzQixJQUFJLHFDQUFpQixFQUFFLENBQUM7QUFFbkUsUUFBUSxDQUFDLGtCQUFrQixFQUFFO0lBQzNCLE1BQU0sQ0FBQztRQUNMLG9CQUFPLENBQUMscUJBQXFCLENBQUMsS0FBSyxDQUFDLENBQUM7UUFDckMsb0JBQU8sQ0FBQyxHQUFHLENBQUMsdUJBQXVCLENBQUMsQ0FBQztJQUN2QyxDQUFDLENBQUMsQ0FBQztJQUVILEVBQUUsQ0FBQyx5QkFBeUIsRUFBRTtRQUM1QixNQUFNLENBQUMsY0FBYyxDQUFDLFlBQVksRUFBRSxDQUFDLENBQUM7SUFDeEMsQ0FBQyxDQUFDLENBQUM7SUFFSCxFQUFFLENBQUMsaUNBQWlDLEVBQUU7UUFDcEMsTUFBTSxDQUFDLGNBQWMsQ0FBQyxTQUFTLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUMsRUFBRSxDQUFDLElBQUksQ0FBQztJQUMzRCxDQUFDLENBQUMsQ0FBQztJQUVILEVBQUUsQ0FBQyxzQ0FBc0MsRUFBRTtRQUN6QyxNQUFNLENBQUMsY0FBYyxDQUFDLGNBQWMsRUFBRSxDQUFDLENBQUMsRUFBRSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFD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