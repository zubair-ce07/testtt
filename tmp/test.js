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
            protractor_1.browser.waitForAngularEnabled(false);
            protractor_1.browser.get('https://www.kayak.com');
            protractor_1.browser.manage().deleteAllCookies();
        });
        it("Select flights from top", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const url = yield homePageObject.clickFlights();
                url.includes('flights');
            });
        });
        it("Should display the origin field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const departureDisplay = yield searchFormObject.getDepartureDisplay();
                departureDisplay.should.equal(true);
            });
        });
        it("Should display the destination field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const destinationDisplay = yield searchFormObject.getDestinationDisplay();
                destinationDisplay.should.equal(true);
            });
        });
        it("Should display the departure date field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const departureDateDispalay = yield searchFormObject.departureDateFieldDisplay();
                departureDateDispalay.should.equal(true);
            });
        });
        it("Should display the return date field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const returnDateDisplay = yield searchFormObject.returnDateFieldDisplay();
                returnDateDisplay.should.equal(true);
            });
        });
        it("Should display ‘Round-trip’ in trip type field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const roundTripType = yield homePageObject.roundTripTypeField();
                roundTripType.should.equal(true);
            });
        });
        it("Switch to ‘One-way’ trip type mode", function () {
            return __awaiter(this, void 0, void 0, function* () {
                homePageObject.changeToOneWayTrip();
                const departureDateDispalay = yield searchFormObject.departureDateFieldDisplay();
                departureDateDispalay.should.equal(true);
            });
        });
        it("Switch to ‘Multi-city’ trip type mode", function () {
            return __awaiter(this, void 0, void 0, function* () {
                homePageObject.changeToMulticityTrip();
                const multicityTripType = yield homePageObject.multiCities();
                multicityTripType.should.equal(true);
            });
        });
        it("Switch to ‘Round-trip’ trip type mode", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.changeToRoundTrip();
                const roundTripType = yield searchFormObject.returnDateFieldDisplay();
                roundTripType.should.equal(true);
            });
        });
        it("Change number of ‘adults’ from travelers field to 9", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.addAdultPassengers(10);
                const adultLimitMessage = yield homePageObject.getAdultsLimitMessage();
                adultLimitMessage.should.equal("Searches cannot have more than 9 adults");
            });
        });
        it("Should display ‘Paris (PAR)’ in origin field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.setDeparture("PAR");
                const departure = yield homePageObject.getDepartureValue();
                departure.should.equal("Paris (PAR)");
            });
        });
        it("Should display ‘New York (NYC)’ in the destination field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.setDestination("NYC");
                const destination = yield homePageObject.getDestinationValue();
                destination.should.equal("New York (NYC)");
            });
        });
        it("Should display accurate date in departure field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.fillDatesDeparture();
                expect(homePageObject.getDepartureDate()).to.eventually.equal(homePageObject.getTripDates(3));
            });
        });
        it("Should display accurate date in return date field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.fillDatesReturn();
                expect(homePageObject.getReturnDate()).to.eventually.equal(homePageObject.getTripDates(6));
            });
        });
        it("Should display all unchecked checkboxes in compare-to block", function () {
            homePageObject.uncheckAllCheckBox();
        });
        it("Should display ‘4 Travelers’ in the travelers field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                homePageObject.decreaseAdultPassengers(6);
                const adultPassengers = yield homePageObject.getAdultPassenger();
                adultPassengers.should.equal(4);
            });
        });
        it("Should display ‘6 Travelers’ in the travelers field", function () {
            homePageObject.addChildPassengers(2);
            const childPassengers = homePageObject.getChildPassenger();
            childPassengers.should.equal(2);
        });
        it("Should display correct filled-in search form on results page", function () {
            return __awaiter(this, void 0, void 0, function* () {
                let searchUrl = yield homePageObject.clickSearch();
                searchUrl.includes('sort=bestflight_a');
            });
        });
        it("Should display the origin field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const departureDisplay = yield searchFormObject.getDepartureDisplay();
                departureDisplay.should.equal(true);
            });
        });
        it("Should display the destination field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const destinationDisplay = yield searchFormObject.getDestinationDisplay();
                destinationDisplay.should.equal(true);
            });
        });
        it("Should display the departure date field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const departureDateDispalay = yield searchFormObject.departureDateFieldDisplay();
                departureDateDispalay.should.equal(true);
            });
        });
        it("Should display the return date field", function () {
            return __awaiter(this, void 0, void 0, function* () {
                const returnDateDisplay = yield searchFormObject.returnDateFieldDisplay();
                returnDateDisplay.should.equal(true);
            });
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
            return __awaiter(this, void 0, void 0, function* () {
                const cheapTime = yield flightsPageObject.getCheapestTime();
                const bestTime = yield flightsPageObject.getBestTime();
                const quickTime = yield flightsPageObject.getQuickestTime();
                yield protractor_1.promise.all([cheapTime, bestTime, quickTime]);
            });
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3Rlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBMEQ7QUFDMUQscURBQWtEO0FBQ2xELDJEQUF3RDtBQUN4RCx5REFBc0Q7QUFHdEQsSUFBSSxJQUFJLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQyxDQUFDO0FBQzNCLElBQUksY0FBYyxHQUFHLE9BQU8sQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO0FBQ2pELElBQUksQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLENBQUM7QUFDekIsSUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQztBQUN6QixJQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7QUFDM0IsSUFBSSxjQUFjLEdBQW1CLElBQUksK0JBQWMsRUFBRSxDQUFDO0FBQzFELElBQUksaUJBQWlCLEdBQXNCLElBQUkscUNBQWlCLEVBQUUsQ0FBQztBQUNuRSxJQUFJLGdCQUFnQixHQUFxQixJQUFJLG1DQUFnQixFQUFFLENBQUM7QUFFaEUsUUFBUSxDQUFDLGtCQUFrQixFQUFFOztRQUMzQixNQUFNLENBQUM7WUFDTCxvQkFBTyxDQUFDLHFCQUFxQixDQUFDLEtBQUssQ0FBQyxDQUFDO1lBQ3JDLG9CQUFPLENBQUMsR0FBRyxDQUFDLHVCQUF1QixDQUFDLENBQUM7WUFDckMsb0JBQU8sQ0FBQyxNQUFNLEVBQUUsQ0FBQyxnQkFBZ0IsRUFBRSxDQUFDO1FBQ3RDLENBQUMsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHlCQUF5QixFQUFFOztnQkFDNUIsTUFBTSxHQUFHLEdBQUcsTUFBTSxjQUFjLENBQUMsWUFBWSxFQUFFLENBQUM7Z0JBQ2hELEdBQUcsQ0FBQyxRQUFRLENBQUMsU0FBUyxDQUFDLENBQUM7WUFDMUIsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxpQ0FBaUMsRUFBRTs7Z0JBQ3BDLE1BQU0sZ0JBQWdCLEdBQUcsTUFBTSxnQkFBZ0IsQ0FBQyxtQkFBbUIsRUFBRSxDQUFDO2dCQUN0RSxnQkFBZ0IsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQ3RDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsc0NBQXNDLEVBQUU7O2dCQUN6QyxNQUFNLGtCQUFrQixHQUFHLE1BQU8sZ0JBQWdCLENBQUMscUJBQXFCLEVBQUUsQ0FBQztnQkFDM0Usa0JBQWtCLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUN4QyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHlDQUF5QyxFQUFFOztnQkFDNUMsTUFBTSxxQkFBcUIsR0FBRyxNQUFNLGdCQUFnQixDQUFDLHlCQUF5QixFQUFFLENBQUM7Z0JBQ2pGLHFCQUFxQixDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDM0MsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxzQ0FBc0MsRUFBRTs7Z0JBQ3pDLE1BQU0saUJBQWlCLEdBQUcsTUFBTSxnQkFBZ0IsQ0FBQyxzQkFBc0IsRUFBRSxDQUFDO2dCQUMxRSxpQkFBaUIsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQ3ZDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsZ0RBQWdELEVBQUU7O2dCQUNuRCxNQUFNLGFBQWEsR0FBRyxNQUFNLGNBQWMsQ0FBQyxrQkFBa0IsRUFBRSxDQUFDO2dCQUNoRSxhQUFhLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUNuQyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLG9DQUFvQyxFQUFFOztnQkFDdkMsY0FBYyxDQUFDLGtCQUFrQixFQUFFLENBQUM7Z0JBQ3BDLE1BQU0scUJBQXFCLEdBQUcsTUFBTSxnQkFBZ0IsQ0FBQyx5QkFBeUIsRUFBRSxDQUFDO2dCQUNqRixxQkFBcUIsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQzNDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsdUNBQXVDLEVBQUU7O2dCQUMxQyxjQUFjLENBQUMscUJBQXFCLEVBQUUsQ0FBQztnQkFDdkMsTUFBTSxpQkFBaUIsR0FBRyxNQUFNLGNBQWMsQ0FBQyxXQUFXLEVBQUUsQ0FBQztnQkFDN0QsaUJBQWlCLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUN2QyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHVDQUF1QyxFQUFFOztnQkFDMUMsTUFBTSxjQUFjLENBQUMsaUJBQWlCLEVBQUUsQ0FBQztnQkFDekMsTUFBTSxhQUFhLEdBQUcsTUFBTSxnQkFBZ0IsQ0FBQyxzQkFBc0IsRUFBRSxDQUFDO2dCQUN0RSxhQUFhLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUNuQyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHFEQUFxRCxFQUFFOztnQkFDeEQsTUFBTSxjQUFjLENBQUMsa0JBQWtCLENBQUMsRUFBRSxDQUFDLENBQUM7Z0JBQzVDLE1BQU0saUJBQWlCLEdBQUcsTUFBTSxjQUFjLENBQUMscUJBQXFCLEVBQUUsQ0FBQztnQkFDdkUsaUJBQWlCLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyx5Q0FBeUMsQ0FBQyxDQUFDO1lBQzVFLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsOENBQThDLEVBQUU7O2dCQUNqRCxNQUFNLGNBQWMsQ0FBQyxZQUFZLENBQUMsS0FBSyxDQUFDLENBQUM7Z0JBQ3pDLE1BQU0sU0FBUyxHQUFHLE1BQU0sY0FBYyxDQUFDLGlCQUFpQixFQUFFLENBQUM7Z0JBQzNELFNBQVMsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLGFBQWEsQ0FBQyxDQUFDO1lBQ3hDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsMERBQTBELEVBQUU7O2dCQUM3RCxNQUFNLGNBQWMsQ0FBQyxjQUFjLENBQUMsS0FBSyxDQUFDLENBQUM7Z0JBQzNDLE1BQU0sV0FBVyxHQUFHLE1BQU0sY0FBYyxDQUFDLG1CQUFtQixFQUFFLENBQUM7Z0JBQy9ELFdBQVcsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLGdCQUFnQixDQUFDLENBQUM7WUFDN0MsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxpREFBaUQsRUFBRTs7Z0JBQ3BELE1BQU0sY0FBYyxDQUFDLGtCQUFrQixFQUFFLENBQUM7Z0JBQzFDLE1BQU0sQ0FBQyxjQUFjLENBQUMsZ0JBQWdCLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUMsS0FBSyxDQUFDLGNBQWMsQ0FBQyxZQUFZLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztZQUNoRyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLG1EQUFtRCxFQUFFOztnQkFDdEQsTUFBTSxjQUFjLENBQUMsZUFBZSxFQUFFLENBQUM7Z0JBQ3ZDLE1BQU0sQ0FBQyxjQUFjLENBQUMsYUFBYSxFQUFFLENBQUMsQ0FBQyxFQUFFLENBQUMsVUFBVSxDQUFDLEtBQUssQ0FBQyxjQUFjLENBQUMsWUFBWSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7WUFDN0YsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyw2REFBNkQsRUFBRTtZQUNoRSxjQUFjLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztRQUN0QyxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxxREFBcUQsRUFBRTs7Z0JBQ3hELGNBQWMsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDLENBQUMsQ0FBQztnQkFDMUMsTUFBTSxlQUFlLEdBQUcsTUFBTSxjQUFjLENBQUMsaUJBQWlCLEVBQUUsQ0FBQztnQkFDakUsZUFBZSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUM7WUFDbEMsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxxREFBcUQsRUFBRTtZQUN4RCxjQUFjLENBQUMsa0JBQWtCLENBQUMsQ0FBQyxDQUFDLENBQUM7WUFDckMsTUFBTSxlQUFlLEdBQUcsY0FBYyxDQUFDLGlCQUFpQixFQUFFLENBQUM7WUFDM0QsZUFBZSxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUM7UUFDbEMsQ0FBQyxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsOERBQThELEVBQUU7O2dCQUNqRSxJQUFJLFNBQVMsR0FBRyxNQUFNLGNBQWMsQ0FBQyxXQUFXLEVBQUUsQ0FBQztnQkFDbkQsU0FBUyxDQUFDLFFBQVEsQ0FBQyxtQkFBbUIsQ0FBQyxDQUFDO1lBQ3hDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFTCxFQUFFLENBQUMsaUNBQWlDLEVBQUU7O2dCQUNwQyxNQUFNLGdCQUFnQixHQUFHLE1BQU0sZ0JBQWdCLENBQUMsbUJBQW1CLEVBQUUsQ0FBQztnQkFDdEUsZ0JBQWdCLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUN0QyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHNDQUFzQyxFQUFFOztnQkFDekMsTUFBTSxrQkFBa0IsR0FBRyxNQUFPLGdCQUFnQixDQUFDLHFCQUFxQixFQUFFLENBQUM7Z0JBQzNFLGtCQUFrQixDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDeEMsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyx5Q0FBeUMsRUFBRTs7Z0JBQzVDLE1BQU0scUJBQXFCLEdBQUcsTUFBTSxnQkFBZ0IsQ0FBQyx5QkFBeUIsRUFBRSxDQUFDO2dCQUNqRixxQkFBcUIsQ0FBQyxNQUFNLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1lBQzNDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsc0NBQXNDLEVBQUU7O2dCQUN6QyxNQUFNLGlCQUFpQixHQUFHLE1BQU0sZ0JBQWdCLENBQUMsc0JBQXNCLEVBQUUsQ0FBQztnQkFDMUUsaUJBQWlCLENBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUN2QyxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHFHQUFxRyxFQUFFOztnQkFDeEcsTUFBTSxVQUFVLEdBQUcsaUJBQWlCLENBQUMsZ0JBQWdCLEVBQUUsQ0FBQztnQkFDeEQsTUFBTSxTQUFTLEdBQUcsaUJBQWlCLENBQUMsWUFBWSxFQUFFLENBQUM7Z0JBQ25ELE1BQU0sVUFBVSxHQUFHLGlCQUFpQixDQUFDLGdCQUFnQixFQUFFLENBQUM7Z0JBQ3hELE1BQU0sb0JBQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQyxVQUFVLEVBQUMsU0FBUyxFQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUM7WUFDdkQsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxvR0FBb0csRUFBRTs7Z0JBQ3ZHLE1BQU0sU0FBUyxHQUFHLE1BQU0saUJBQWlCLENBQUMsZUFBZSxFQUFFLENBQUM7Z0JBQzVELE1BQU0sUUFBUSxHQUFHLE1BQU0saUJBQWlCLENBQUMsV0FBVyxFQUFFLENBQUM7Z0JBQ3ZELE1BQU0sU0FBUyxHQUFHLE1BQU0saUJBQWlCLENBQUMsZUFBZSxFQUFFLENBQUM7Z0JBQzVELE1BQU0sb0JBQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQyxTQUFTLEVBQUUsUUFBUSxFQUFFLFNBQVMsQ0FBQyxDQUFDLENBQUM7WUFDdEQsQ0FBQztTQUFBLENBQUMsQ0FBQztJQUNMLENBQUM7Q0FBQSxDQUFDLENBQUMifQ==