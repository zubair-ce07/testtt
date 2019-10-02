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
class HomePageObject {
    constructor() {
        this.flights = protractor_1.element(protractor_1.by.className("js-vertical-flights"));
        this.originField = protractor_1.element(protractor_1.by.css('div[id$="origin-airport-display"]'));
        this.destination = protractor_1.element(protractor_1.by.css('div[id$="H9Tw-destination-airport-display"]'));
        this.departureDateField = protractor_1.element(protractor_1.by.css('div[id$=dateRangeInput-display-start]'));
        this.roundTripField = protractor_1.element(protractor_1.by.css('div[id$="sZO2-switch-option-1"]'));
        this.switchOptions = protractor_1.element(protractor_1.by.css("div[id$=switch-display]"));
        this.switchOneWayOption = protractor_1.element(protractor_1.by.css("li[id$=switch-option-2]"));
        this.switchMultiCityOption = protractor_1.element(protractor_1.by.css("li[id$=switch-option-3]"));
        this.multiCitiesGrid = protractor_1.element(protractor_1.by.css("div[id$=mf8B-cabin_type0-display-status]"));
        this.switchRoundTripOption = protractor_1.element(protractor_1.by.css("li[id$=switch-option-1]"));
        this.travelersGrid = protractor_1.element(protractor_1.by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
        this.addAdultButton = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
        this.passengerErrorText = protractor_1.element(protractor_1.by.css("div[id$=travelersAboveForm-errorMessage]"));
        this.originInput = protractor_1.element.all(protractor_1.by.name('origin')).first();
        this.originSelect = protractor_1.element(protractor_1.by.css("ul[class='flight-smarty'] li"));
        this.originText = protractor_1.element(protractor_1.by.css('div[id$="origin-airport-display-inner"]'));
        this.destinationField = protractor_1.element(protractor_1.by.css('div[id$="destination-airport-display"]'));
        this.destinationInput = protractor_1.element.all(protractor_1.by.name('destination')).first();
        this.destinationSelect = protractor_1.element(protractor_1.by.css("div[id$='destination-airport-smartbox-dropdown'] li"));
        this.destinationText = protractor_1.element(protractor_1.by.css('div[id$="destination-airport-display-inner"]'));
        this.passengersDropdown = protractor_1.element(protractor_1.by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
        this.passengerAdultDecrement = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-adults'] .decrementor-js"));
        this.passengerAdultText = protractor_1.element(protractor_1.by.css('div[id$="travelersAboveForm-adults"]'));
        this.passengerChildInput = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-child'] .incrementor-js"));
        this.passengerChildText = protractor_1.element(protractor_1.by.css('div[id$="travelersAboveForm-child"]'));
        this.departureDateInput = protractor_1.element(protractor_1.by.css("div[id$='depart-input']"));
        this.returnDateInput = protractor_1.element(protractor_1.by.css("div[id$='return-input']"));
        this.returnDateField = protractor_1.element(protractor_1.by.css('div[id$=dateRangeInput-display-end]'));
        this.searchButton = protractor_1.element(protractor_1.by.css("button[aria-label='Search flights']"));
        this.checkbox = protractor_1.element(protractor_1.by.css("button[aria-label='Disable results comparison for this search']"));
    }
    clickFlights() {
        this.flights.click();
    }
    getOrigin() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.originField.isDisplayed();
        });
    }
    getDestination() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.destination.isDisplayed();
        });
    }
    departureField() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.departureDateField.isDisplayed();
        });
    }
    returnField() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.returnDateField.isDisplayed();
        });
    }
    roundTripTypeField() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.roundTripField.getAttribute("aria-selected");
        });
    }
    clickSwitch() {
        this.switchOptions.click();
        protractor_1.browser.sleep(1000);
    }
    clickOneWay() {
        this.switchOneWayOption.click();
        protractor_1.browser.sleep(1000);
    }
    clickMultiCity() {
        this.switchMultiCityOption.click();
        protractor_1.browser.sleep(1000);
    }
    multiCities() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.multiCitiesGrid.isDisplayed();
        });
    }
    clickRoundTrip() {
        this.switchRoundTripOption.click();
        protractor_1.browser.sleep(1000);
    }
    clickTravelersGrid() {
        this.travelersGrid.click();
        protractor_1.browser.sleep(1000);
    }
    addAdultPassengers(adult) {
        for (let i = 0; i < adult - 1; i++) {
            this.addAdultButton.click();
        }
    }
    getAdultsLimitMessage() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.passengerErrorText.getText();
        });
    }
    clickOriginField() {
        this.originField.click();
        protractor_1.browser.sleep(1000);
    }
    fillOrigin(origin) {
        this.originInput.clear();
        this.originInput.click();
        this.originInput.sendKeys(origin);
        protractor_1.browser.sleep(1000);
    }
    selectOrigin() {
        this.originSelect.click();
        protractor_1.browser.sleep(1000);
    }
    getOriginValue() {
        return this.originText.getText();
    }
    clickDestinationField() {
        this.destinationField.click();
        protractor_1.browser.sleep(1000);
    }
    fillDestination(destination) {
        this.destinationInput.click();
        this.destinationInput.clear();
        this.destinationInput.sendKeys(destination);
        protractor_1.browser.sleep(1000);
    }
    selectDestination() {
        this.destinationSelect.click();
        protractor_1.browser.sleep(2000);
    }
    getDestinationValue() {
        return this.destinationText.getText();
    }
    clickPassengersDropdown() {
        this.passengersDropdown.click();
        protractor_1.browser.sleep(1000);
    }
    decreaseAdultPassengers(adult) {
        for (let i = 0; i < adult - 1; i++) {
            this.passengerAdultDecrement.click();
        }
    }
    getAdultPassenger() {
        return this.passengerAdultText.getAttribute("aria-valuenow");
    }
    addChildPassengers(child) {
        for (let i = 0; i < child; i++) {
            this.passengerChildInput.click();
        }
    }
    getChildPassenger() {
        return this.passengerChildText.getAttribute("aria-valuenow");
    }
    clickDepartureField() {
        this.departureDateField.click();
        protractor_1.browser.sleep(1000);
    }
    fillDatesDeparture() {
        this.departureDateInput.click();
        this.departureDateInput.clear();
        this.departureDateInput.sendKeys(this.setTripDates(3));
        protractor_1.browser.sleep(2000);
    }
    getDepartureDate() {
        return this.departureDateField.getText();
    }
    getTripDates(tripDate) {
        const todaysDate = new Date();
        const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        todaysDate.setDate(todaysDate.getDate() + tripDate);
        const departureDayName = weekdays[todaysDate.getDay()];
        return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
    }
    fillDatesReturn() {
        this.returnDateInput.click();
        this.returnDateInput.clear();
        protractor_1.browser.sleep(1000);
        this.returnDateInput.sendKeys(this.setTripDates(6));
        protractor_1.browser.sleep(1000);
    }
    setTripDates(daysToTrip) {
        const todaysDate = new Date();
        todaysDate.setDate(todaysDate.getDate() + daysToTrip);
        let dd = todaysDate.getDate().toString();
        let mm = (todaysDate.getMonth() + 1).toString();
        let yyyy = todaysDate.getFullYear().toString();
        if (todaysDate.getDate() < 10) {
            dd = "0" + dd;
        }
        if (mm < '10') {
            mm = "0" + mm;
        }
        return (mm + "/" + dd + "/" + yyyy);
    }
    getReturnDate() {
        return this.returnDateField.getText();
    }
    clickSearch() {
        this.searchButton.click();
        protractor_1.browser.sleep(5000);
    }
    switchTabs() {
        protractor_1.browser.getAllWindowHandles().then((tabs) => {
            if (tabs.length > 1) {
                protractor_1.browser.driver.switchTo().window(tabs[0]);
                protractor_1.browser.driver.close();
                protractor_1.browser.driver.switchTo().window(tabs[1]);
            }
        });
    }
    uncheckAllCheckBox() {
        this.checkbox.click();
        protractor_1.browser.sleep(2000);
    }
}
exports.HomePageObject = HomePageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaG9tZVBhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9ob21lUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUFvRjtBQUVwRixNQUFhLGNBQWM7SUFBM0I7UUFFQyxZQUFPLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsZ0JBQVcsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLG1DQUFtQyxDQUFDLENBQUMsQ0FBQztRQUNsRixnQkFBVyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsNkNBQTZDLENBQUMsQ0FBQyxDQUFDO1FBQzVGLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsdUNBQXVDLENBQUMsQ0FBQyxDQUFDO1FBQzdGLG1CQUFjLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxpQ0FBaUMsQ0FBQyxDQUFDLENBQUM7UUFDbkYsa0JBQWEsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQztRQUMxRSx1QkFBa0IsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQztRQUMvRSwwQkFBcUIsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQztRQUNsRixvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMENBQTBDLENBQUMsQ0FBQyxDQUFDO1FBQzdGLDBCQUFxQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUJBQXlCLENBQUMsQ0FBQyxDQUFDO1FBQ2xGLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQywrQ0FBK0MsQ0FBQyxDQUFDLENBQUM7UUFDdEcsbUJBQWMsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHNEQUFzRCxDQUFDLENBQUMsQ0FBQztRQUN4Ryx1QkFBa0IsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDBDQUEwQyxDQUFDLENBQUMsQ0FBQztRQUNoRyxnQkFBVyxHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDcEUsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDhCQUE4QixDQUFDLENBQUMsQ0FBQztRQUM5RSxlQUFVLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5Q0FBeUMsQ0FBQyxDQUFDLENBQUM7UUFDdkYscUJBQWdCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx3Q0FBd0MsQ0FBQyxDQUFDLENBQUM7UUFDNUYscUJBQWdCLEdBQWtCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxJQUFJLENBQUMsYUFBYSxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5RSxzQkFBaUIsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHFEQUFxRCxDQUFDLENBQUMsQ0FBQztRQUMxRyxvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsOENBQThDLENBQUMsQ0FBQyxDQUFDO1FBQ2pHLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsK0NBQStDLENBQUMsQ0FBQyxDQUFDO1FBQzNHLDRCQUF1QixHQUFtQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsc0RBQXNELENBQUMsQ0FBQyxDQUFDO1FBQ2xILHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsc0NBQXNDLENBQUMsQ0FBQyxDQUFDO1FBQzVGLHdCQUFtQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscURBQXFELENBQUMsQ0FBQyxDQUFDO1FBQzVHLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscUNBQXFDLENBQUMsQ0FBQyxDQUFDO1FBQzNGLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUJBQXlCLENBQUMsQ0FBQyxDQUFDO1FBQy9FLG9CQUFlLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5QkFBeUIsQ0FBQyxDQUFDLENBQUM7UUFDNUUsb0JBQWUsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHFDQUFxQyxDQUFDLENBQUMsQ0FBQztRQUN4RixpQkFBWSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscUNBQXFDLENBQUMsQ0FBQyxDQUFDO1FBQ3JGLGFBQVEsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLGlFQUFpRSxDQUFDLENBQUMsQ0FBQztJQTBNOUcsQ0FBQztJQXhNQSxZQUFZO1FBQ1gsSUFBSSxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsQ0FBQztJQUN0QixDQUFDO0lBRUssU0FBUzs7WUFDZCxPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxXQUFXLEVBQUUsQ0FBQztRQUM3QyxDQUFDO0tBQUE7SUFFSyxjQUFjOztZQUNuQixPQUFPLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxXQUFXLEVBQUUsQ0FBQztRQUM3QyxDQUFDO0tBQUE7SUFFSyxjQUFjOztZQUNuQixPQUFPLE1BQU0sSUFBSSxDQUFDLGtCQUFrQixDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ3BELENBQUM7S0FBQTtJQUVLLFdBQVc7O1lBQ2hCLE9BQU8sTUFBTSxJQUFJLENBQUMsZUFBZSxDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ2pELENBQUM7S0FBQTtJQUVLLGtCQUFrQjs7WUFDdkIsT0FBTyxNQUFNLElBQUksQ0FBQyxjQUFjLENBQUMsWUFBWSxDQUFDLGVBQWUsQ0FBQyxDQUFDO1FBQ2hFLENBQUM7S0FBQTtJQUVELFdBQVc7UUFDVixJQUFJLENBQUMsYUFBYSxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzNCLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxXQUFXO1FBQ1YsSUFBSSxDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ2hDLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxjQUFjO1FBQ2IsSUFBSSxDQUFDLHFCQUFxQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ25DLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFSyxXQUFXOztZQUNoQixPQUFPLE1BQU0sSUFBSSxDQUFDLGVBQWUsQ0FBQyxXQUFXLEVBQUUsQ0FBQztRQUNqRCxDQUFDO0tBQUE7SUFFRCxjQUFjO1FBQ2IsSUFBSSxDQUFDLHFCQUFxQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ25DLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxrQkFBa0I7UUFDakIsSUFBSSxDQUFDLGFBQWEsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMzQixvQkFBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUNyQixDQUFDO0lBRUQsa0JBQWtCLENBQUMsS0FBYTtRQUMvQixLQUFJLElBQUksQ0FBQyxHQUFXLENBQUMsRUFBRSxDQUFDLEdBQUcsS0FBSyxHQUFHLENBQUMsRUFBRSxDQUFDLEVBQUUsRUFBRTtZQUMxQyxJQUFJLENBQUMsY0FBYyxDQUFDLEtBQUssRUFBRSxDQUFDO1NBQzVCO0lBQ0YsQ0FBQztJQUVLLHFCQUFxQjs7WUFDMUIsT0FBTyxNQUFNLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUNoRCxDQUFDO0tBQUE7SUFFRCxnQkFBZ0I7UUFDZixJQUFJLENBQUMsV0FBVyxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ3pCLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxVQUFVLENBQUMsTUFBYztRQUN4QixJQUFJLENBQUMsV0FBVyxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ3pCLElBQUksQ0FBQyxXQUFXLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDekIsSUFBSSxDQUFDLFdBQVcsQ0FBQyxRQUFRLENBQUMsTUFBTSxDQUFDLENBQUM7UUFDbEMsb0JBQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDckIsQ0FBQztJQUVELFlBQVk7UUFDWCxJQUFJLENBQUMsWUFBWSxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzFCLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxjQUFjO1FBQ2IsT0FBTyxJQUFJLENBQUMsVUFBVSxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ2xDLENBQUM7SUFFRCxxQkFBcUI7UUFDcEIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzlCLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxlQUFlLENBQUMsV0FBbUI7UUFDbEMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzlCLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5QixJQUFJLENBQUMsZ0JBQWdCLENBQUMsUUFBUSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1FBQzVDLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxpQkFBaUI7UUFDaEIsSUFBSSxDQUFDLGlCQUFpQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQy9CLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxtQkFBbUI7UUFDbEIsT0FBTyxJQUFJLENBQUMsZUFBZSxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ3ZDLENBQUM7SUFFRCx1QkFBdUI7UUFDdEIsSUFBSSxDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ2hDLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCx1QkFBdUIsQ0FBQyxLQUFhO1FBQ3BDLEtBQUksSUFBSSxDQUFDLEdBQVcsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLEdBQUcsQ0FBQyxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQzFDLElBQUksQ0FBQyx1QkFBdUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztTQUNyQztJQUNGLENBQUM7SUFFRCxpQkFBaUI7UUFDaEIsT0FBTyxJQUFJLENBQUMsa0JBQWtCLENBQUMsWUFBWSxDQUFDLGVBQWUsQ0FBQyxDQUFDO0lBQzlELENBQUM7SUFFRCxrQkFBa0IsQ0FBQyxLQUFhO1FBQy9CLEtBQUksSUFBSSxDQUFDLEdBQVcsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLEVBQUUsQ0FBQyxFQUFFLEVBQUU7WUFDdEMsSUFBSSxDQUFDLG1CQUFtQixDQUFDLEtBQUssRUFBRSxDQUFDO1NBQ2pDO0lBQ0YsQ0FBQztJQUVELGlCQUFpQjtRQUNoQixPQUFPLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxZQUFZLENBQUMsZUFBZSxDQUFDLENBQUM7SUFDOUQsQ0FBQztJQUVELG1CQUFtQjtRQUNsQixJQUFJLENBQUMsa0JBQWtCLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDaEMsb0JBQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDckIsQ0FBQztJQUVELGtCQUFrQjtRQUNqQixJQUFJLENBQUMsa0JBQWtCLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDaEMsSUFBSSxDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ2hDLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBQ3ZELG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3JCLENBQUM7SUFFRCxnQkFBZ0I7UUFDZixPQUFPLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUMxQyxDQUFDO0lBRUQsWUFBWSxDQUFDLFFBQWdCO1FBQzVCLE1BQU0sVUFBVSxHQUFHLElBQUksSUFBSSxFQUFFLENBQUM7UUFDOUIsTUFBTSxRQUFRLEdBQWtCLENBQUMsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDaEYsVUFBVSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLEdBQUcsUUFBUSxDQUFDLENBQUM7UUFDcEQsTUFBTSxnQkFBZ0IsR0FBRyxRQUFRLENBQUMsVUFBVSxDQUFDLE1BQU0sRUFBRSxDQUFDLENBQUM7UUFDdkQsT0FBTyxDQUFDLGdCQUFnQixHQUFHLEdBQUcsR0FBRyxDQUFDLFVBQVUsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDLENBQUMsR0FBRyxHQUFHLEdBQUcsQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQyxDQUFDO0lBQ2hHLENBQUM7SUFFRCxlQUFlO1FBQ2QsSUFBSSxDQUFDLGVBQWUsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM3QixJQUFJLENBQUMsZUFBZSxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzdCLG9CQUFPLENBQUMsS0FBSyxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3BCLElBQUksQ0FBQyxlQUFlLENBQUMsUUFBUSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUNwRCxvQkFBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUNyQixDQUFDO0lBRUQsWUFBWSxDQUFDLFVBQWtCO1FBQzlCLE1BQU0sVUFBVSxHQUFTLElBQUksSUFBSSxFQUFFLENBQUM7UUFDbEMsVUFBVSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLEdBQUcsVUFBVSxDQUFDLENBQUM7UUFDdEQsSUFBSSxFQUFFLEdBQVcsVUFBVSxDQUFDLE9BQU8sRUFBRSxDQUFDLFFBQVEsRUFBRSxDQUFDO1FBQ2pELElBQUksRUFBRSxHQUFXLENBQUMsVUFBVSxDQUFDLFFBQVEsRUFBRSxHQUFDLENBQUMsQ0FBQyxDQUFDLFFBQVEsRUFBRSxDQUFDO1FBQ3RELElBQUksSUFBSSxHQUFXLFVBQVUsQ0FBQyxXQUFXLEVBQUUsQ0FBQyxRQUFRLEVBQUUsQ0FBQztRQUN2RCxJQUFHLFVBQVUsQ0FBQyxPQUFPLEVBQUUsR0FBRyxFQUFFLEVBQUU7WUFDNUIsRUFBRSxHQUFHLEdBQUcsR0FBRyxFQUFFLENBQUM7U0FDakI7UUFDRCxJQUFHLEVBQUUsR0FBRyxJQUFJLEVBQUU7WUFDVixFQUFFLEdBQUcsR0FBRyxHQUFHLEVBQUUsQ0FBQztTQUNmO1FBQ0QsT0FBTyxDQUFDLEVBQUUsR0FBRyxHQUFHLEdBQUcsRUFBRSxHQUFHLEdBQUcsR0FBRyxJQUFJLENBQUMsQ0FBQztJQUN2QyxDQUFDO0lBRUQsYUFBYTtRQUNaLE9BQU8sSUFBSSxDQUFDLGVBQWUsQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUN2QyxDQUFDO0lBRUQsV0FBVztRQUNWLElBQUksQ0FBQyxZQUFZLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDMUIsb0JBQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDckIsQ0FBQztJQUVELFVBQVU7UUFDVCxvQkFBTyxDQUFDLG1CQUFtQixFQUFFLENBQUMsSUFBSSxDQUFDLENBQUMsSUFBSSxFQUFFLEVBQUU7WUFDM0MsSUFBRyxJQUFJLENBQUMsTUFBTSxHQUFHLENBQUMsRUFBRTtnQkFDbkIsb0JBQU8sQ0FBQyxNQUFNLENBQUMsUUFBUSxFQUFFLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO2dCQUMxQyxvQkFBTyxDQUFDLE1BQU0sQ0FBQyxLQUFLLEVBQUUsQ0FBQztnQkFDdkIsb0JBQU8sQ0FBQyxNQUFNLENBQUMsUUFBUSxFQUFFLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO2FBQzFDO1FBQ0YsQ0FBQyxDQUFDLENBQUM7SUFDSixDQUFDO0lBRUQsa0JBQWtCO1FBQ2pCLElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDdEIsb0JBQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDckIsQ0FBQztDQUNEO0FBek9ELHdDQXlPQyJ9