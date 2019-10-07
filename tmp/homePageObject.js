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
const commonPageObject_1 = require("./commonPageObject");
class HomePageObject {
    constructor() {
        this.commonPageObject = new commonPageObject_1.CommonPageObject();
        this.flights = protractor_1.element(protractor_1.by.className("js-vertical-flights"));
        this.roundTripField = protractor_1.element(protractor_1.by.css('div[id$="switch-option-1"]'));
        this.switchOptions = protractor_1.element(protractor_1.by.css("div[id$=switch-display]"));
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
        this.originText = protractor_1.element(protractor_1.by.css('div[id$="origin-airport-display-inner"]'));
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
        this.searchButton = protractor_1.element(protractor_1.by.css("button[aria-label='Search flights']"));
        this.checkbox = protractor_1.element(protractor_1.by.css("button[aria-label='Disable results comparison for this search']"));
        this.destinationList = protractor_1.element.all(protractor_1.by.className('item-info')).first();
        this.EC = protractor_1.protractor.ExpectedConditions;
    }
    clickFlights() {
        return __awaiter(this, void 0, void 0, function* () {
            this.flights.click();
            var url = yield protractor_1.browser.getCurrentUrl();
            return yield protractor_1.browser.getCurrentUrl();
        });
    }
    roundTripTypeField() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.roundTripField.getAttribute("aria-selected");
        });
    }
    changeToOneWayTrip() {
        this.commonPageObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.commonPageObject.waitUntillElementAppears(this.switchOneWayOption);
        this.switchOneWayOption.click();
    }
    changeToMulticityTrip() {
        this.commonPageObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.commonPageObject.waitUntillElementAppears(this.switchMultiCityOption);
        this.switchMultiCityOption.click();
    }
    changeToRoundTrip() {
        this.commonPageObject.waitUntillElementAppears(this.switchOptions);
        this.switchOptions.click();
        this.commonPageObject.waitUntillElementAppears(this.switchRoundTripOption);
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
        return __awaiter(this, void 0, void 0, function* () {
            yield this.commonPageObject.waitUntillElementAppears(this.travelersGrid);
            yield this.travelersGrid.click();
            yield this.commonPageObject.waitUntillElementAppears(this.addAdultButton);
            for (let i = 0; i < adult - 1; i++) {
                yield this.addAdultButton.click();
            }
        });
    }
    getAdultsLimitMessage() {
        return __awaiter(this, void 0, void 0, function* () {
            this.commonPageObject.waitUntillElementAppears(this.passengerErrorText);
            const errorMsg = this.passengerErrorText.getText();
            yield this.travelersGrid.sendKeys(protractor_1.Key.ESCAPE);
            return errorMsg;
        });
    }
    setDeparture() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.commonPageObject.waitUntillElementAppears(this.commonPageObject.departureField);
            yield this.commonPageObject.departureField.click();
            yield this.commonPageObject.waitUntillElementAppears(this.originInput);
            yield this.originInput.clear();
            yield this.originInput.sendKeys("PAR");
            yield this.commonPageObject.waitUntillElementAppears(this.originSelect);
            yield this.originSelect.click();
        });
    }
    setDestination() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.commonPageObject.waitUntillElementAppears(this.commonPageObject.destinationField);
            yield this.commonPageObject.destinationField.click();
            yield this.commonPageObject.waitUntillElementAppears(this.destinationInput);
            yield this.destinationInput.clear();
            yield this.destinationInput.sendKeys("NYC");
            yield this.commonPageObject.waitUntillElementAppears(this.destinationSelect);
            yield this.destinationSelect.click();
        });
    }
    getOriginValue() {
        return __awaiter(this, void 0, void 0, function* () {
            this.commonPageObject.waitUntillElementAppears(this.originText);
            return yield this.originText.getText();
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
            this.commonPageObject.waitUntillElementAppears(this.destinationText);
            return yield this.destinationText.getText();
        });
    }
    clickPassengersDropdown() {
        this.passengersDropdown.click();
    }
    decreaseAdultPassengers(adult) {
        this.commonPageObject.waitUntillElementAppears(this.passengersDropdown);
        this.passengersDropdown.click();
        this.commonPageObject.waitUntillElementAppears(this.passengerAdultDecrement);
        for (let i = 0; i < adult - 1; i++) {
            this.passengerAdultDecrement.click();
        }
    }
    getAdultPassenger() {
        return __awaiter(this, void 0, void 0, function* () {
            this.commonPageObject.waitUntillElementAppears(this.passengerAdultText);
            return this.passengerAdultText.getAttribute("aria-valuenow");
        });
    }
    addChildPassengers(child) {
        this.commonPageObject.waitUntillElementAppears(this.passengerChildInput);
        for (let i = 0; i < child; i++) {
            this.passengerChildInput.click();
        }
    }
    getChildPassenger() {
        return this.passengerChildText.getAttribute("aria-valuenow");
    }
    clickDepartureField() {
        this.commonPageObject.departureDateField.click();
    }
    fillDatesDeparture() {
        this.commonPageObject.waitUntillElementAppears(this.commonPageObject.departureDateField);
        this.commonPageObject.departureDateField.click();
        this.commonPageObject.waitUntillElementAppears(this.departureDateInput);
        this.departureDateInput.clear();
        this.departureDateInput.sendKeys(this.setTripDates(3));
    }
    getDepartureDate() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.commonPageObject.departureDateField.getText();
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
        this.commonPageObject.waitUntillElementAppears(this.returnDateInput);
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
            return this.commonPageObject.returnDateField.getText();
        });
    }
    clickSearch() {
        return __awaiter(this, void 0, void 0, function* () {
            this.searchButton.click();
            yield this.commonPageObject.waitUntillElementAppears(protractor_1.browser.getCurrentUrl());
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
        return __awaiter(this, void 0, void 0, function* () {
            this.commonPageObject.waitUntillElementAppears(this.checkbox);
            this.checkbox.click();
        });
    }
}
exports.HomePageObject = HomePageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaG9tZVBhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9ob21lUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUF1SDtBQUN2SCx5REFBc0Q7QUFHdEQsTUFBYSxjQUFjO0lBQTNCO1FBQ0MscUJBQWdCLEdBQXFCLElBQUksbUNBQWdCLEVBQUUsQ0FBQztRQUM1RCxZQUFPLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsbUJBQWMsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDRCQUE0QixDQUFDLENBQUMsQ0FBQztRQUM5RSxrQkFBYSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUJBQXlCLENBQUMsQ0FBQyxDQUFDO1FBQzFFLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMzRiwwQkFBcUIsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5QkFBeUIsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDOUYsb0JBQWUsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLDBDQUEwQyxDQUFDLENBQUMsQ0FBQztRQUM3RixvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsNkJBQTZCLENBQUMsQ0FBQyxDQUFBO1FBQy9FLDBCQUFxQixHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5RixrQkFBYSxHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLCtDQUErQyxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUNsSCxtQkFBYyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsc0RBQXNELENBQUMsQ0FBQyxDQUFDO1FBQ3hHLHVCQUFrQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMENBQTBDLENBQUMsQ0FBQyxDQUFDO1FBQ2hHLGdCQUFXLEdBQWtCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUNwRSxpQkFBWSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsOEJBQThCLENBQUMsQ0FBQyxDQUFDO1FBQzlFLGVBQVUsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlDQUF5QyxDQUFDLENBQUMsQ0FBQztRQUN2RixxQkFBZ0IsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLElBQUksQ0FBQyxhQUFhLENBQUMsQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzlFLHNCQUFpQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscURBQXFELENBQUMsQ0FBQyxDQUFDO1FBQzFHLG9CQUFlLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyw4Q0FBOEMsQ0FBQyxDQUFDLENBQUM7UUFDakcsdUJBQWtCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQywrQ0FBK0MsQ0FBQyxDQUFDLENBQUM7UUFDM0csNEJBQXVCLEdBQW1CLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxzREFBc0QsQ0FBQyxDQUFDLENBQUM7UUFDbEgsdUJBQWtCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxzQ0FBc0MsQ0FBQyxDQUFDLENBQUM7UUFDNUYsd0JBQW1CLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxREFBcUQsQ0FBQyxDQUFDLENBQUM7UUFDNUcsdUJBQWtCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxQ0FBcUMsQ0FBQyxDQUFDLENBQUM7UUFDM0YsdUJBQWtCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5QkFBeUIsQ0FBQyxDQUFDLENBQUM7UUFDL0Usb0JBQWUsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlCQUF5QixDQUFDLENBQUMsQ0FBQztRQUM1RSxpQkFBWSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscUNBQXFDLENBQUMsQ0FBQyxDQUFDO1FBQ3JGLGFBQVEsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLGlFQUFpRSxDQUFDLENBQUMsQ0FBQztRQUU3RyxvQkFBZSxHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLFdBQVcsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDaEYsT0FBRSxHQUFHLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7SUF3TXBDLENBQUM7SUF0TU0sWUFBWTs7WUFDakIsSUFBSSxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsQ0FBQztZQUNyQixJQUFJLEdBQUcsR0FBRyxNQUFNLG9CQUFPLENBQUMsYUFBYSxFQUFFLENBQUM7WUFDeEMsT0FBTyxNQUFNLG9CQUFPLENBQUMsYUFBYSxFQUFFLENBQUM7UUFDdEMsQ0FBQztLQUFBO0lBRUssa0JBQWtCOztZQUN2QixPQUFPLE1BQU0sSUFBSSxDQUFDLGNBQWMsQ0FBQyxZQUFZLENBQUMsZUFBZSxDQUFDLENBQUM7UUFDaEUsQ0FBQztLQUFBO0lBRUQsa0JBQWtCO1FBQ2pCLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMsYUFBYSxDQUFDLENBQUM7UUFDbkUsSUFBSSxDQUFDLGFBQWEsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMzQixJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGtCQUFrQixDQUFDLENBQUM7UUFDeEUsSUFBSSxDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO0lBQ2pDLENBQUM7SUFFRCxxQkFBcUI7UUFDcEIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxhQUFhLENBQUMsQ0FBQztRQUNuRSxJQUFJLENBQUMsYUFBYSxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzNCLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMscUJBQXFCLENBQUMsQ0FBQztRQUMzRSxJQUFJLENBQUMscUJBQXFCLENBQUMsS0FBSyxFQUFFLENBQUM7SUFDcEMsQ0FBQztJQUVELGlCQUFpQjtRQUNoQixJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGFBQWEsQ0FBQyxDQUFDO1FBQ25FLElBQUksQ0FBQyxhQUFhLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDM0IsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDO1FBQzNFLElBQUksQ0FBQyxxQkFBcUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztJQUNwQyxDQUFDO0lBRUQsV0FBVztRQUNWLElBQUksQ0FBQyxhQUFhLENBQUMsS0FBSyxFQUFFLENBQUM7SUFDNUIsQ0FBQztJQUVLLFdBQVc7O1lBQ2hCLE9BQU8sTUFBTSxJQUFJLENBQUMsZUFBZSxDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ2pELENBQUM7S0FBQTtJQUVELGNBQWM7UUFDYixJQUFJLENBQUMscUJBQXFCLENBQUMsS0FBSyxFQUFFLENBQUM7SUFDcEMsQ0FBQztJQUVLLGtCQUFrQixDQUFDLEtBQWE7O1lBQ3JDLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxhQUFhLENBQUMsQ0FBQztZQUN6RSxNQUFNLElBQUksQ0FBQyxhQUFhLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDakMsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGNBQWMsQ0FBQyxDQUFDO1lBQzFFLEtBQUksSUFBSSxDQUFDLEdBQVcsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLEdBQUcsQ0FBQyxFQUFFLENBQUMsRUFBRSxFQUFFO2dCQUMxQyxNQUFNLElBQUksQ0FBQyxjQUFjLENBQUMsS0FBSyxFQUFFLENBQUM7YUFDbEM7UUFDRixDQUFDO0tBQUE7SUFFSyxxQkFBcUI7O1lBQzFCLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMsa0JBQWtCLENBQUMsQ0FBQztZQUN4RSxNQUFNLFFBQVEsR0FBSSxJQUFJLENBQUMsa0JBQWtCLENBQUMsT0FBTyxFQUFFLENBQUM7WUFDcEQsTUFBTSxJQUFJLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxnQkFBRyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBQzlDLE9BQU8sUUFBUSxDQUFDO1FBQ2pCLENBQUM7S0FBQTtJQUVLLFlBQVk7O1lBQ2pCLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxjQUFjLENBQUMsQ0FBQztZQUMzRixNQUFNLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxjQUFjLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDbkQsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1lBQ3ZFLE1BQU0sSUFBSSxDQUFDLFdBQVcsQ0FBQyxLQUFLLEVBQUUsQ0FBQztZQUMvQixNQUFNLElBQUksQ0FBQyxXQUFXLENBQUMsUUFBUSxDQUFDLEtBQUssQ0FBQyxDQUFDO1lBQ3ZDLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztZQUN4RSxNQUFNLElBQUksQ0FBQyxZQUFZLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDakMsQ0FBQztLQUFBO0lBRUssY0FBYzs7WUFDbkIsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLGdCQUFnQixDQUFDLENBQUM7WUFDN0YsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsZ0JBQWdCLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDckQsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLENBQUM7WUFDNUUsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDcEMsTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsUUFBUSxDQUFDLEtBQUssQ0FBQyxDQUFDO1lBQzVDLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxpQkFBaUIsQ0FBQyxDQUFDO1lBQzdFLE1BQU0sSUFBSSxDQUFDLGlCQUFpQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ3RDLENBQUM7S0FBQTtJQUVLLGNBQWM7O1lBQ25CLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMsVUFBVSxDQUFDLENBQUM7WUFDaEUsT0FBTyxNQUFNLElBQUksQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDeEMsQ0FBQztLQUFBO0lBRUQsZUFBZSxDQUFDLFdBQW1CO1FBQ2xDLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM5QixJQUFJLENBQUMsZ0JBQWdCLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDOUIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsQ0FBQyxXQUFXLENBQUMsQ0FBQztJQUM3QyxDQUFDO0lBRUQsaUJBQWlCO1FBQ2hCLElBQUksQ0FBQyxpQkFBaUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztJQUNoQyxDQUFDO0lBRU0sbUJBQW1COztZQUN6QixJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGVBQWUsQ0FBQyxDQUFDO1lBQ3JFLE9BQU8sTUFBTSxJQUFJLENBQUMsZUFBZSxDQUFDLE9BQU8sRUFBRSxDQUFDO1FBQzdDLENBQUM7S0FBQTtJQUVELHVCQUF1QjtRQUN0QixJQUFJLENBQUMsa0JBQWtCLENBQUMsS0FBSyxFQUFFLENBQUM7SUFDakMsQ0FBQztJQUVELHVCQUF1QixDQUFDLEtBQWE7UUFDcEMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO1FBQ3hFLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUNoQyxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLHVCQUF1QixDQUFDLENBQUM7UUFDN0UsS0FBSSxJQUFJLENBQUMsR0FBVyxDQUFDLEVBQUUsQ0FBQyxHQUFHLEtBQUssR0FBRyxDQUFDLEVBQUUsQ0FBQyxFQUFFLEVBQUU7WUFDMUMsSUFBSSxDQUFDLHVCQUF1QixDQUFDLEtBQUssRUFBRSxDQUFDO1NBQ3JDO0lBQ0YsQ0FBQztJQUVLLGlCQUFpQjs7WUFDdEIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO1lBQ3hFLE9BQU8sSUFBSSxDQUFDLGtCQUFrQixDQUFDLFlBQVksQ0FBQyxlQUFlLENBQUMsQ0FBQztRQUM5RCxDQUFDO0tBQUE7SUFFRCxrQkFBa0IsQ0FBQyxLQUFhO1FBQy9CLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUN6RSxLQUFJLElBQUksQ0FBQyxHQUFXLENBQUMsRUFBRSxDQUFDLEdBQUcsS0FBSyxFQUFFLENBQUMsRUFBRSxFQUFFO1lBQ3RDLElBQUksQ0FBQyxtQkFBbUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztTQUNqQztJQUNGLENBQUM7SUFFRCxpQkFBaUI7UUFDaEIsT0FBTyxJQUFJLENBQUMsa0JBQWtCLENBQUMsWUFBWSxDQUFDLGVBQWUsQ0FBQyxDQUFDO0lBQzlELENBQUM7SUFFRCxtQkFBbUI7UUFDbEIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO0lBQ2xELENBQUM7SUFFRCxrQkFBa0I7UUFDakIsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO1FBQ3pGLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxrQkFBa0IsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUNqRCxJQUFJLENBQUMsZ0JBQWdCLENBQUMsd0JBQXdCLENBQUMsSUFBSSxDQUFDLGtCQUFrQixDQUFDLENBQUM7UUFDeEUsSUFBSSxDQUFDLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ2hDLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ3hELENBQUM7SUFFSyxnQkFBZ0I7O1lBQ3JCLE9BQU8sTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsa0JBQWtCLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDakUsQ0FBQztLQUFBO0lBRUQsWUFBWSxDQUFDLFFBQWdCO1FBQzVCLE1BQU0sVUFBVSxHQUFHLElBQUksSUFBSSxFQUFFLENBQUM7UUFDOUIsTUFBTSxRQUFRLEdBQWtCLENBQUMsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDbEYsVUFBVSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLEdBQUcsUUFBUSxDQUFDLENBQUM7UUFDcEQsTUFBTSxnQkFBZ0IsR0FBRyxRQUFRLENBQUMsVUFBVSxDQUFDLE1BQU0sRUFBRSxDQUFDLENBQUM7UUFDdkQsT0FBTyxDQUFDLGdCQUFnQixHQUFHLEdBQUcsR0FBRyxDQUFDLFVBQVUsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDLENBQUMsR0FBRyxHQUFHLEdBQUcsQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQyxDQUFDO0lBQzlGLENBQUM7SUFFRCxlQUFlO1FBQ2QsSUFBSSxDQUFDLGdCQUFnQixDQUFDLHdCQUF3QixDQUFDLElBQUksQ0FBQyxlQUFlLENBQUMsQ0FBQztRQUNyRSxJQUFJLENBQUMsZUFBZSxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzdCLElBQUksQ0FBQyxlQUFlLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDN0IsSUFBSSxDQUFDLGVBQWUsQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ3JELENBQUM7SUFFRCxZQUFZLENBQUMsVUFBa0I7UUFDOUIsTUFBTSxVQUFVLEdBQVMsSUFBSSxJQUFJLEVBQUUsQ0FBQztRQUNsQyxVQUFVLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUUsR0FBRyxVQUFVLENBQUMsQ0FBQztRQUN0RCxJQUFJLEVBQUUsR0FBVyxVQUFVLENBQUMsT0FBTyxFQUFFLENBQUMsUUFBUSxFQUFFLENBQUM7UUFDakQsSUFBSSxFQUFFLEdBQVcsQ0FBQyxVQUFVLENBQUMsUUFBUSxFQUFFLEdBQUMsQ0FBQyxDQUFDLENBQUMsUUFBUSxFQUFFLENBQUM7UUFDdEQsSUFBSSxJQUFJLEdBQVcsVUFBVSxDQUFDLFdBQVcsRUFBRSxDQUFDLFFBQVEsRUFBRSxDQUFDO1FBQ3ZELElBQUcsVUFBVSxDQUFDLE9BQU8sRUFBRSxHQUFHLEVBQUUsRUFBRTtZQUM1QixFQUFFLEdBQUcsR0FBRyxHQUFHLEVBQUUsQ0FBQztTQUNqQjtRQUNELElBQUcsRUFBRSxHQUFHLElBQUksRUFBRTtZQUNWLEVBQUUsR0FBRyxHQUFHLEdBQUcsRUFBRSxDQUFDO1NBQ2Y7UUFDRCxPQUFPLENBQUMsRUFBRSxHQUFHLEdBQUcsR0FBRyxFQUFFLEdBQUcsR0FBRyxHQUFHLElBQUksQ0FBQyxDQUFDO0lBQ3ZDLENBQUM7SUFFSyxhQUFhOztZQUNsQixPQUFPLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyxlQUFlLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDeEQsQ0FBQztLQUFBO0lBRUssV0FBVzs7WUFDaEIsSUFBSSxDQUFDLFlBQVksQ0FBQyxLQUFLLEVBQUUsQ0FBQztZQUMxQixNQUFNLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxvQkFBTyxDQUFDLGFBQWEsRUFBRSxDQUFDLENBQUM7WUFDOUUsT0FBTyxNQUFNLG9CQUFPLENBQUMsYUFBYSxFQUFFLENBQUM7UUFDdEMsQ0FBQztLQUFBO0lBRUQsVUFBVTtRQUNULG9CQUFPLENBQUMsbUJBQW1CLEVBQUUsQ0FBQyxJQUFJLENBQUMsQ0FBQyxJQUFJLEVBQUUsRUFBRTtZQUMzQyxJQUFHLElBQUksQ0FBQyxNQUFNLEdBQUcsQ0FBQyxFQUFFO2dCQUNuQixvQkFBTyxDQUFDLE1BQU0sQ0FBQyxRQUFRLEVBQUUsQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7Z0JBQzFDLG9CQUFPLENBQUMsTUFBTSxDQUFDLEtBQUssRUFBRSxDQUFDO2dCQUN2QixvQkFBTyxDQUFDLE1BQU0sQ0FBQyxRQUFRLEVBQUUsQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7YUFDMUM7UUFDRixDQUFDLENBQUMsQ0FBQztJQUNKLENBQUM7SUFFSyxrQkFBa0I7O1lBQ3RCLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQyx3QkFBd0IsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLENBQUM7WUFDL0QsSUFBSSxDQUFDLFFBQVEsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUN2QixDQUFDO0tBQUE7Q0FDRDtBQXRPRCx3Q0FzT0MifQ==