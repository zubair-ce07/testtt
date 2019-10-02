import {browser, element, by, protractor, promise, ElementFinder} from 'protractor';

export class HomePageObject {

	flights: ElementFinder = element(by.className("js-vertical-flights"));
	originField: ElementFinder = element(by.css('div[id$="origin-airport-display"]'));
	destination: ElementFinder = element(by.css('div[id$="H9Tw-destination-airport-display"]'));
	departureDateField: ElementFinder = element(by.css('div[id$=dateRangeInput-display-start]'));
	roundTripField: ElementFinder = element(by.css('div[id$="sZO2-switch-option-1"]'));
	switchOptions: ElementFinder = element(by.css("div[id$=switch-display]"));
	switchOneWayOption: ElementFinder = element(by.css("li[id$=switch-option-2]"));
	switchMultiCityOption: ElementFinder = element(by.css("li[id$=switch-option-3]"));
	multiCitiesGrid: ElementFinder = element(by.css("div[id$=mf8B-cabin_type0-display-status]"));
	switchRoundTripOption: ElementFinder = element(by.css("li[id$=switch-option-1]"));
	travelersGrid: ElementFinder = element(by.className("Flights-Search-StyleJamFlightTravelerDropdown"));
	addAdultButton: ElementFinder = element(by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
	passengerErrorText: ElementFinder = element(by.css("div[id$=travelersAboveForm-errorMessage]"));
	originInput: ElementFinder = element.all(by.name('origin')).first();
	originSelect: ElementFinder = element(by.css("ul[class='flight-smarty'] li"));
	originText: ElementFinder = element(by.css('div[id$="origin-airport-display-inner"]'));
	destinationField: ElementFinder = element(by.css('div[id$="destination-airport-display"]'));
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
	returnDateField: ElementFinder = element(by.css('div[id$=dateRangeInput-display-end]'));
	searchButton: ElementFinder = element(by.css("button[aria-label='Search flights']"));
	checkbox: ElementFinder = element(by.css("button[aria-label='Disable results comparison for this search']"));

	clickFlights(): void {
		this.flights.click();
	}

	async getOrigin(): Promise<Boolean> {
		return await this.originField.isDisplayed();
	}

	async getDestination(): Promise<Boolean> {
		return await this.destination.isDisplayed();
	}

	async departureField(): Promise<Boolean> {
		return await this.departureDateField.isDisplayed();
	}

	async returnField(): Promise<Boolean> {
		return await this.returnDateField.isDisplayed();
	}

	async roundTripTypeField(): Promise<string> {
		return await this.roundTripField.getAttribute("aria-selected");
	}

	clickSwitch(): void {
		this.switchOptions.click();
		browser.sleep(1000);
	}

	clickOneWay(): void {
		this.switchOneWayOption.click();
		browser.sleep(1000);
	}

	clickMultiCity(): void {
		this.switchMultiCityOption.click();
		browser.sleep(1000);
	}

	async multiCities(): Promise<boolean> {
		return await this.multiCitiesGrid.isDisplayed();
	}

	clickRoundTrip(): void {
		this.switchRoundTripOption.click();
		browser.sleep(1000);
	}

	clickTravelersGrid(): void {
		this.travelersGrid.click();
		browser.sleep(1000);
	}

	addAdultPassengers(adult: number): void {
		for(let i: number = 0; i < adult - 1; i++) {
			this.addAdultButton.click();
		}
	}

	async getAdultsLimitMessage(): Promise<string> {
		return await this.passengerErrorText.getText();
	}

	clickOriginField(): void {
		this.originField.click();
		browser.sleep(1000);
	}

	fillOrigin(origin: string): void {
		this.originInput.clear();
		this.originInput.click();
		this.originInput.sendKeys(origin);
		browser.sleep(1000);
	}

	selectOrigin(): void {
		this.originSelect.click();
		browser.sleep(1000);
	}

	getOriginValue(): promise.Promise<string> {
		return this.originText.getText();
	}

	clickDestinationField(): void {
		this.destinationField.click();
		browser.sleep(1000);
	}

	fillDestination(destination: string): void {
		this.destinationInput.click();
		this.destinationInput.clear();
		this.destinationInput.sendKeys(destination);
		browser.sleep(1000);
	}

	selectDestination(): void {
		this.destinationSelect.click();
		browser.sleep(2000);
	}

	getDestinationValue(): promise.Promise<string> {
		return this.destinationText.getText();
	}

	clickPassengersDropdown(): void {
		this.passengersDropdown.click();
		browser.sleep(1000);
	}

	decreaseAdultPassengers(adult: number): void {
		for(let i: number = 0; i < adult - 1; i++) {
			this.passengerAdultDecrement.click();
		}
	}

	getAdultPassenger(): promise.Promise<string> {
		return this.passengerAdultText.getAttribute("aria-valuenow");
	}

	addChildPassengers(child: number): void {
		for(let i: number = 0; i < child; i++) {
			this.passengerChildInput.click();
		}
	}

	getChildPassenger(): promise.Promise<string> {
		return this.passengerChildText.getAttribute("aria-valuenow");
	}

	clickDepartureField(): void {
		this.departureDateField.click();
		browser.sleep(1000);
	}

	fillDatesDeparture(): void {
		this.departureDateInput.click();
		this.departureDateInput.clear();
		this.departureDateInput.sendKeys(this.setTripDates(3));
		browser.sleep(2000);
	}

	getDepartureDate(): promise.Promise<string> {
		return this.departureDateField.getText();
	}

	getTripDates(tripDate: number): string {
		const todaysDate = new Date();
		const weekdays: Array<String> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    todaysDate.setDate(todaysDate.getDate() + tripDate);
    const departureDayName = weekdays[todaysDate.getDay()];
    return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
	}

	fillDatesReturn(): void {
		this.returnDateInput.click();
		this.returnDateInput.clear();
		browser.sleep(1000);
		this.returnDateInput.sendKeys(this.setTripDates(6));
		browser.sleep(1000);
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
	
	getReturnDate(): promise.Promise<string> {
		return this.returnDateField.getText();
	}

	clickSearch(): void {
		this.searchButton.click();
		browser.sleep(5000);
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
		this.checkbox.click();
		browser.sleep(2000);
	}
}
