import {browser, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions, Key} from 'protractor';
import { SearchFormObject } from './searchFormObject';

export class HomePageObject {
	searchFormObject : SearchFormObject = new SearchFormObject();
	flights: ElementFinder = element(by.className("js-vertical-flights"));
	roundTripField: ElementFinder = element.all(by.css('div .Common-Widgets-Select-StyleJamSelect')).first();
	switchOptions: ElementFinder = element.all(by.css("div[id$=switch-display]")).first();
	switchOneWayOption: ElementFinder = element.all(by.css("li[id$=switch-option-2]")).first();
	switchMultiCityOption: ElementFinder = element.all(by.css("li[id$=switch-option-3]")).first();
	multiCitiesGrid: ElementFinder = element(by.css("div[id$=mf8B-cabin_type0-display-status]"));
	multiCityOption: ElementFinder = element(by.css('div[data-value="multicity"]'))
	switchRoundTripOption: ElementFinder = element.all(by.css("li[id$=switch-option-1]")).first();
	travelersGrid: ElementFinder = element.all(by.className("Flights-Search-StyleJamFlightTravelerDropdown")).first();
	addAdultButton: ElementFinder = element(by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
	passengerErrorText: ElementFinder = element(by.css("div[id$=travelersAboveForm-errorMessage]"));
	originInput: ElementFinder = element.all(by.name('origin')).first();
	originSelect: ElementFinder = element(by.css("[class='flight-smarty'] li"));
	departureText: ElementFinder = element.all(by.css('div[id$="origin-airport-display-inner"]')).first();
	destinationInput: ElementFinder = element.all(by.name('destination')).first();
	destinationSelect: ElementFinder = element.all(by.css("div[id$='destination-airport-smartbox-dropdown'] li")).first();
	destinationText: ElementFinder = element.all(by.css('div[id$="destination-airport-display-inner"]')).first();
	passengersDropdown: ElementFinder = element(by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
	passengerAdultDecrement: ElementFinder =  element(by.css("div[id$='travelersAboveForm-adults'] .decrementor-js"));
	passengerAdultText: ElementFinder = element(by.css('div[id$="travelersAboveForm-adults"]'));
	passengerChildInput: ElementFinder = element(by.css("div[id$='travelersAboveForm-child'] .incrementor-js"));
	passengerChildText: ElementFinder = element(by.css('div[id$="travelersAboveForm-child"]'));
	departureDateInput: ElementFinder = element(by.css("div[id$='depart-input']"));
	returnDateInput: ElementFinder = element(by.css("div[id$='return-input']"));
	searchButton: ElementFinder = element(by.css("button[aria-label='Search flights']"));
	checkbox: ElementFinder = element(by.css("button[aria-label='Disable results comparison for this search']"));

	clickFlights(): promise.Promise<string> {
		this.flights.click();
		return browser.getCurrentUrl();
	}
	
	changeToOneWayTrip() {
		this.searchFormObject.waitUntillElementAppears(this.switchOptions);
		this.switchOptions.click();
		this.searchFormObject.waitUntillElementAppears(this.switchOneWayOption);
		this.switchOneWayOption.click();
	}

	changeToMulticityTrip(): void {
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

	clickSwitch(): void {
	  this.switchOptions.click();
	}

	async multiCities(): Promise<boolean> {
		return await this.multiCityOption.isDisplayed();
	}

	clickRoundTrip(): void {
		this.switchRoundTripOption.click();
	}

	addAdultPassengers(adult: number): void {
		this.searchFormObject.waitUntillElementAppears(this.travelersGrid);
		this.travelersGrid.click();
		this.searchFormObject.waitUntillElementAppears(this.addAdultButton);
		for(let i: number = 0; i < adult - 1; i++) {
			this.addAdultButton.click();
		}
	}

	async getAdultsLimitMessage(): Promise<string> {
		await this.searchFormObject.waitUntillElementAppears(this.passengerErrorText);
		const errorMsg = this.passengerErrorText.getText();
		// this.passengerErrorText.sendKeys(Key.ESCAPE);
		return errorMsg;
	}

	async setDeparture(departure: string) {
		await this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureField);
		this.searchFormObject.departureField.click();
		this.searchFormObject.waitUntillElementAppears(this.originInput);
		this.originInput.sendKeys(Key.BACK_SPACE);
		this.originInput.sendKeys(Key.BACK_SPACE);
		this.originInput.sendKeys(departure);
		await this.searchFormObject.waitUntillElementAppears(this.originSelect);
		this.originSelect.click();
	}

	async setDestination(destination: string) {
		await this.searchFormObject.waitUntillElementAppears(this.searchFormObject.destinationField);
		this.searchFormObject.destinationField.click();
		this.searchFormObject.waitUntillElementAppears(this.destinationInput);
		this.destinationInput.clear();
		this.destinationInput.sendKeys(destination);
		await this.searchFormObject.waitUntillElementAppears(this.destinationSelect);
		this.destinationSelect.click();
	}

	async getDepartureValue(): Promise<string> {
		await this.searchFormObject.waitUntillElementAppears(this.departureText);
		return await this.departureText.getText();
	}

	fillDestination(destination: string): void {
		this.destinationInput.click();
		this.destinationInput.clear();
		this.destinationInput.sendKeys(destination);
	}

	selectDestination(): void {
		this.destinationSelect.click();
	}

  async getDestinationValue(): Promise<string> {
    await this.searchFormObject.waitUntillElementAppears(this.destinationText);
    return await this.destinationText.getText();
	}

	clickPassengersDropdown(): void {
		this.passengersDropdown.click();
	}

	decreaseAdultPassengers(adult: number): void {
		this.searchFormObject.waitUntillElementAppears(this.passengersDropdown);
		this.passengersDropdown.click();
		this.searchFormObject.waitUntillElementAppears(this.passengerAdultDecrement);
		for(let i: number = 0; i < adult - 1; i++) {
			this.passengerAdultDecrement.click();
		}
	}

	getAdultPassenger(): promise.Promise<string> {
		this.searchFormObject.waitUntillElementAppears(this.passengerAdultText);
		return this.passengerAdultText.getAttribute("aria-valuenow");
	}

	addChildPassengers(child: number): void {
		this.searchFormObject.waitUntillElementAppears(this.passengerChildInput);
		for(let i: number = 0; i < child; i++) {
			this.passengerChildInput.click();
		}
	}

	getChildPassenger(): promise.Promise<string> {
		return this.passengerChildText.getAttribute("aria-valuenow");
	}

	clickDepartureField(): void {
		this.searchFormObject.departureDateField.click();
	}

  async fillDatesDeparture(): Promise<void> {
		await this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureDateField);
		this.searchFormObject.departureDateField.click();
		await this.searchFormObject.waitUntillElementAppears(this.departureDateInput);
		this.departureDateInput.clear();
		await this.departureDateInput.sendKeys(this.setTripDates(3));
	}

	getDepartureDate(): ElementFinder {
		return this.searchFormObject.departureDateField;
	}

	getTripDates(tripDate: number): string {
		const todaysDate = new Date();
		const weekdays: Array<String> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
		todaysDate.setDate(todaysDate.getDate() + tripDate);
		const departureDayName = weekdays[todaysDate.getDay()];
		return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
	}

	fillDatesReturn(): void {
		this.searchFormObject.waitUntillElementAppears(this.returnDateInput);
		this.returnDateInput.click();
		this.returnDateInput.clear();
		this.returnDateInput.sendKeys(this.setTripDates(6));
	}

	setTripDates(daysToTrip: number): string {
    const todaysDate: Date = new Date();
    todaysDate.setDate(todaysDate.getDate() + daysToTrip); 
    let dd: string = todaysDate.getDate().toString();
    let mm: string = (todaysDate.getMonth()+1).toString();
    let yyyy: string = todaysDate.getFullYear().toString();
    if(todaysDate.getDate() < 10) {
      dd = "0" + dd;
    }
    if(mm < '10') {
      mm = "0" + mm;
    }
    return (mm + "/" + dd + "/" + yyyy);
	}
	
	async getReturnDate(): Promise<string> {
		return this.searchFormObject.returnDateField.getText();
	}

	async clickSearch(): Promise<string> {
		this.searchButton.click();
		browser.sleep(4000);
		return await browser.getCurrentUrl();
	}

	switchTabs(): void {
		browser.getAllWindowHandles().then((tabs) => {
			if(tabs.length > 1) {
				browser.driver.switchTo().window(tabs[0]);
				browser.driver.close();
				browser.driver.switchTo().window(tabs[1]);
			}
		});
	}

	uncheckAllCheckBox() {
	 	this.searchFormObject.waitUntillElementAppears(this.checkbox);
		this.checkbox.click();
	}
}
