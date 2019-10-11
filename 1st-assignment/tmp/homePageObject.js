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
const searchFormObject_1 = require("./searchFormObject");
class HomePageObject {
    constructor() {
        this.searchFormObject = new searchFormObject_1.SearchFormObject();
        this.flights = protractor_1.element(protractor_1.by.className("js-vertical-flights"));
        this.roundTripField = protractor_1.element.all(protractor_1.by.css('div .Common-Widgets-Select-StyleJamSelect')).first();
        this.switchOptions = protractor_1.element.all(protractor_1.by.css("div[id$=switch-display]")).first();
        this.switchOneWayOption = protractor_1.element.all(protractor_1.by.css("li[id$=switch-option-2]")).first();
        this.switchMultiCityOption = protractor_1.element.all(protractor_1.by.css("li[id$=switch-option-3]")).first();
        this.multiCitiesGrid = protractor_1.element(protractor_1.by.css("div[id$=mf8B-cabin_type0-display-status]"));
        this.multiCityOption = protractor_1.element(protractor_1.by.css('div[data-value="multicity"]'));
        this.switchRoundTripOption = protractor_1.element.all(protractor_1.by.css("li[id$=switch-option-1]")).first();
        this.travelersGrid = protractor_1.element.all(protractor_1.by.className("Flights-Search-StyleJamFlightTravelerDropdown")).first();
        this.addAdultButton = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
        this.passengerErrorText = protractor_1.element(protractor_1.by.css("div[id$=travelersAboveForm-errorMessage]"));
        this.originInput = protractor_1.element.all(protractor_1.by.name('origin')).first();
        this.originSelect = protractor_1.element(protractor_1.by.css("ul[class='flight-smarty'] li"));
        this.departureText = protractor_1.element.all(protractor_1.by.css('div[id$="origin-airport-display-inner"]')).first();
        this.destinationInput = protractor_1.element.all(protractor_1.by.name('destination')).first();
        this.destinationSelect = protractor_1.element.all(protractor_1.by.css("div[id$='destination-airport-smartbox-dropdown'] li")).first();
        this.destinationText = protractor_1.element.all(protractor_1.by.css('div[id$="destination-airport-display-inner"]')).first();
        this.passengersDropdown = protractor_1.element(protractor_1.by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
        this.passengerAdultDecrement = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-adults'] .decrementor-js"));
        this.passengerAdultText = protractor_1.element(protractor_1.by.css('div[id$="travelersAboveForm-adults"]'));
        this.passengerChildInput = protractor_1.element(protractor_1.by.css("div[id$='travelersAboveForm-child'] .incrementor-js"));
        this.passengerChildText = protractor_1.element(protractor_1.by.css('div[id$="travelersAboveForm-child"]'));
        this.departureDateInput = protractor_1.element(protractor_1.by.css("div[id$='depart-input']"));
        this.returnDateInput = protractor_1.element(protractor_1.by.css("div[id$='return-input']"));
        this.searchButton = protractor_1.element(protractor_1.by.css("button[aria-label='Search flights']"));
        this.checkbox = protractor_1.element(protractor_1.by.css("button[aria-label='Disable results comparison for this search']"));
    }
    clickFlights() {
        this.flights.click();
        return protractor_1.browser.getCurrentUrl();
    }
    changeToOneWayTrip() {
        this.searchFormObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.searchFormObject.waitUntillElementAppears(this.switchOneWayOption);
        this.switchOneWayOption.click();
    }
    changeToMulticityTrip() {
        this.searchFormObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.searchFormObject.waitUntillElementAppears(this.switchMultiCityOption);
        this.switchMultiCityOption.click();
    }
    changeToRoundTrip() {
        this.searchFormObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.searchFormObject.waitUntillElementAppears(this.switchRoundTripOption);
        this.switchRoundTripOption.click();
    }
    clickSwitch() {
        this.switchOptions.click();
    }
    multiCities() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.multiCityOption.isDisplayed();
        });
    }
    clickRoundTrip() {
        this.switchRoundTripOption.click();
    }
    addAdultPassengers(adult) {
        this.searchFormObject.waitUntillElementAppears(this.travelersGrid);
        this.travelersGrid.click();
        this.searchFormObject.waitUntillElementAppears(this.addAdultButton);
        for (let i = 0; i < adult - 1; i++) {
            this.addAdultButton.click();
        }
    }
    getAdultsLimitMessage() {
        this.searchFormObject.waitUntillElementAppears(this.passengerErrorText);
        const errorMsg = this.passengerErrorText.getText();
        this.passengerErrorText.sendKeys(protractor_1.Key.ESCAPE);
        return errorMsg;
    }
    setDeparture(departure) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureField);
            this.searchFormObject.departureField.click();
            this.searchFormObject.waitUntillElementAppears(this.originInput);
            this.originInput.clear();
            this.originInput.sendKeys(departure);
            yield this.searchFormObject.waitUntillElementAppears(this.originSelect);
            this.originSelect.click();
        });
    }
    setDestination(destination) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.searchFormObject.waitUntillElementAppears(this.searchFormObject.destinationField);
            this.searchFormObject.destinationField.click();
            this.searchFormObject.waitUntillElementAppears(this.destinationInput);
            this.destinationInput.clear();
            this.destinationInput.sendKeys(destination);
            yield this.searchFormObject.waitUntillElementAppears(this.destinationSelect);
            this.destinationSelect.click();
        });
    }
    getDepartureValue() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.searchFormObject.waitUntillElementAppears(this.departureText);
            return yield this.departureText.getText();
        });
    }
    fillDestination(destination) {
        this.destinationInput.click();
        this.destinationInput.clear();
        this.destinationInput.sendKeys(destination);
    }
    selectDestination() {
        this.destinationSelect.click();
    }
    getDestinationValue() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.searchFormObject.waitUntillElementAppears(this.destinationText);
            return yield this.destinationText.getText();
        });
    }
    clickPassengersDropdown() {
        this.passengersDropdown.click();
    }
    decreaseAdultPassengers(adult) {
        this.searchFormObject.waitUntillElementAppears(this.passengersDropdown);
        this.passengersDropdown.click();
        this.searchFormObject.waitUntillElementAppears(this.passengerAdultDecrement);
        for (let i = 0; i < adult - 1; i++) {
            this.passengerAdultDecrement.click();
        }
    }
    getAdultPassenger() {
        this.searchFormObject.waitUntillElementAppears(this.passengerAdultText);
        return this.passengerAdultText.getAttribute("aria-valuenow");
    }
    addChildPassengers(child) {
        this.searchFormObject.waitUntillElementAppears(this.passengerChildInput);
        for (let i = 0; i < child; i++) {
            this.passengerChildInput.click();
        }
    }
    getChildPassenger() {
        return this.passengerChildText.getAttribute("aria-valuenow");
    }
    clickDepartureField() {
        this.searchFormObject.departureDateField.click();
    }
    fillDatesDeparture() {
        this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureDateField);
        this.searchFormObject.departureDateField.click();
        this.searchFormObject.waitUntillElementAppears(this.departureDateInput);
        this.departureDateInput.clear();
        this.departureDateInput.sendKeys(this.setTripDates(3));
    }
    getDepartureDate() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.searchFormObject.departureDateField.getText();
        });
    }
    getTripDates(tripDate) {
        const todaysDate = new Date();
        const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        todaysDate.setDate(todaysDate.getDate() + tripDate);
        const departureDayName = weekdays[todaysDate.getDay()];
        return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
    }
    fillDatesReturn() {
        this.searchFormObject.waitUntillElementAppears(this.returnDateInput);
        this.returnDateInput.click();
        this.returnDateInput.clear();
        this.returnDateInput.sendKeys(this.setTripDates(6));
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
        return __awaiter(this, void 0, void 0, function* () {
            return this.searchFormObject.returnDateField.getText();
        });
    }
    clickSearch() {
        return __awaiter(this, void 0, void 0, function* () {
            this.searchButton.click();
            protractor_1.browser.sleep(4000);
            return yield protractor_1.browser.getCurrentUrl();
        });
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
        this.searchFormObject.waitUntillElementAppears(this.checkbox);
        this.checkbox.click();
    }
}
exports.HomePageObject = HomePageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaG9tZVBhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9ob21lUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUF1SDtBQUN2SCx5REFBc0Q7QUFFdEQsTUFBYSxjQUFjO0lBQTNCO1FBQ0MscUJBQWdCLEdBQXNCLElBQUksbUNBQWdCLEVBQUUsQ0FBQztRQUM3RCxZQUFPLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsbUJBQWMsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQywyQ0FBMkMsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDekcsa0JBQWEsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5QkFBeUIsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDdEYsdUJBQWtCLEdBQWtCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUJBQXlCLENBQUMsQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzNGLDBCQUFxQixHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5RixvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMENBQTBDLENBQUMsQ0FBQyxDQUFDO1FBQzdGLG9CQUFlLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyw2QkFBNkIsQ0FBQyxDQUFDLENBQUE7UUFDL0UsMEJBQXFCLEdBQWtCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUJBQXlCLENBQUMsQ0FBQyxDQUFDLEtBQUssRUFB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