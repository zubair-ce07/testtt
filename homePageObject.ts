import {browser, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions, Key} from 'protractor';
import { CommonPageObject } from './commonPageObject';
import { escape } from 'querystring';

export class HomePageObject {
	commonPageObject: CommonPageObject = new CommonPageObject();
	flights: ElementFinder = element(by.className("js-vertical-flights"));
	roundTripField: ElementFinder = element(by.css('div[id$="switch-option-1"]'));
	switchOptions: ElementFinder = element(by.css("div[id$=switch-display]"));
	switchOneWayOption: ElementFinder = element.all(by.css("li[id$=switch-option-2]")).first();
	switchMultiCityOption: ElementFinder = element.all(by.css("li[id$=switch-option-3]")).first();
	multiCitiesGrid: ElementFinder = element(by.css("div[id$=mf8B-cabin_type0-display-status]"));
	multiCityOption: ElementFinder = element(by.css('div[data-value="multicity"]'))
	switchRoundTripOption: ElementFinder = element.all(by.css("li[id$=switch-option-1]")).first();
	travelersGrid: ElementFinder = element.all(by.className("Flights-Search-StyleJamFlightTravelerDropdown")).first();
	addAdultButton: ElementFinder = element(by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
	passengerErrorText: ElementFinder = element(by.css("div[id$=travelersAboveForm-errorMessage]"));
	originInput: ElementFinder = element.all(by.name('origin')).first();
	originSelect: ElementFinder = element(by.css("ul[class='flight-smarty'] li"));
	originText: ElementFinder = element(by.css('div[id$="origin-airport-display-inner"]'));
	destinationInput: ElementFinder = element.all(by.name('destination')).first();
	destinationSelect: ElementFinder = element(by.css("div[id$='destination-airport-smartbox-dropdown'] li"));
	destinationText: ElementFinder = element(by.css('div[id$="destination-airport-display-inner"]'));
	passengersDropdown: ElementFinder = element(by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
	passengerAdultDecrement: ElementFinder =  element(by.css("div[id$='travelersAboveForm-adults'] .decrementor-js"));
	passengerAdultText: ElementFinder = element(by.css('div[id$="travelersAboveForm-adults"]'));
	passengerChildInput: ElementFinder = element(by.css("div[id$='travelersAboveForm-child'] .incrementor-js"));
	passengerChildText: ElementFinder = element(by.css('div[id$="travelersAboveForm-child"]'));
	departureDateInput: ElementFinder = element(by.css("div[id$='depart-input']"));
	returnDateInput: ElementFinder = element(by.css("div[id$='return-input']"));
	searchButton: ElementFinder = element(by.css("button[aria-label='Search flights']"));
	checkbox: ElementFinder = element(by.css("button[aria-label='Disable results comparison for this search']"));

	destinationList: ElementFinder = element.all(by.className('item-info')).first();
	EC = protractor.ExpectedConditions;

	async clickFlights(): Promise<string> {
		this.flights.click();
		var url = await browser.getCurrentUrl();
		return await browser.getCurrentUrl();
	}

	async roundTripTypeField(): Promise<string> {
		return await this.roundTripField.getAttribute("aria-selected");
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

	clickSwitch(): void {
		this.switchOptions.click();
	}

	async multiCities(): Promise<boolean> {
		return await this.multiCityOption.isDisplayed();
	}

	clickRoundTrip(): void {
		this.switchRoundTripOption.click();
	}

	async addAdultPassengers(adult: number): Promise<void> {
		await this.commonPageObject.waitUntillElementAppears(this.travelersGrid);
		await this.travelersGrid.click();
		await this.commonPageObject.waitUntillElementAppears(this.addAdultButton);
		for(let i: number = 0; i < adult - 1; i++) {
			await this.addAdultButton.click();
		}
	}

	async getAdultsLimitMessage(): Promise<string> {
		this.commonPageObject.waitUntillElementAppears(this.passengerErrorText);
		const errorMsg =  this.passengerErrorText.getText();
		await this.travelersGrid.sendKeys(Key.ESCAPE);
		return errorMsg;
	}

	async setDeparture() {
		await this.commonPageObject.waitUntillElementAppears(this.commonPageObject.departureField);
		await this.commonPageObject.departureField.click();
		await this.commonPageObject.waitUntillElementAppears(this.originInput);
		await this.originInput.clear();
		await this.originInput.sendKeys("PAR");
		await this.commonPageObject.waitUntillElementAppears(this.originSelect);
		await this.originSelect.click();
	}

	async setDestination() {
		await this.commonPageObject.waitUntillElementAppears(this.commonPageObject.destinationField);
		await this.commonPageObject.destinationField.click();
		await this.commonPageObject.waitUntillElementAppears(this.destinationInput);
		await this.destinationInput.clear();
		await this.destinationInput.sendKeys("NYC");
		await this.commonPageObject.waitUntillElementAppears(this.destinationSelect);
		await this.destinationSelect.click();
	}

	async getOriginValue(): Promise<string> {
		this.commonPageObject.waitUntillElementAppears(this.originText);
		return await this.originText.getText();
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
		this.commonPageObject.waitUntillElementAppears(this.destinationText);
		return await this.destinationText.getText();
	}

	clickPassengersDropdown(): void {
		this.passengersDropdown.click();
	}

	decreaseAdultPassengers(adult: number): void {
		this.commonPageObject.waitUntillElementAppears(this.passengersDropdown);
		this.passengersDropdown.click();
		this.commonPageObject.waitUntillElementAppears(this.passengerAdultDecrement);
		for(let i: number = 0; i < adult - 1; i++) {
			this.passengerAdultDecrement.click();
		}
	}

	async getAdultPassenger(): Promise<string> {
		this.commonPageObject.waitUntillElementAppears(this.passengerAdultText);
		return this.passengerAdultText.getAttribute("aria-valuenow");
	}

	addChildPassengers(child: number): void {
		this.commonPageObject.waitUntillElementAppears(this.passengerChildInput);
		for(let i: number = 0; i < child; i++) {
			this.passengerChildInput.click();
		}
	}

	getChildPassenger(): promise.Promise<string> {
		return this.passengerChildText.getAttribute("aria-valuenow");
	}

	clickDepartureField(): void {
		this.commonPageObject.departureDateField.click();
	}

	fillDatesDeparture(): void {
		this.commonPageObject.waitUntillElementAppears(this.commonPageObject.departureDateField);
		this.commonPageObject.departureDateField.click();
		this.commonPageObject.waitUntillElementAppears(this.departureDateInput);
		this.departureDateInput.clear();
		this.departureDateInput.sendKeys(this.setTripDates(3));
	}

	async getDepartureDate(): Promise<string> {
		return await this.commonPageObject.departureDateField.getText();
	}

	getTripDates(tripDate: number): string {
		const todaysDate = new Date();
		const weekdays: Array<String> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
		todaysDate.setDate(todaysDate.getDate() + tripDate);
		const departureDayName = weekdays[todaysDate.getDay()];
		return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
	}

	fillDatesReturn(): void {
		this.commonPageObject.waitUntillElementAppears(this.returnDateInput);
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
		return this.commonPageObject.returnDateField.getText();
	}

	async clickSearch(): Promise<string> {
		this.searchButton.click();
		await this.commonPageObject.waitUntillElementAppears(browser.getCurrentUrl());
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

	async uncheckAllCheckBox() {
	 	this.commonPageObject.waitUntillElementAppears(this.checkbox);
		this.checkbox.click();
	}
}
