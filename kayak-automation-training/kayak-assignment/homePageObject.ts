import {browser, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions, Key, ElementArrayFinder} from 'protractor';
import { SearchFormObject } from './searchFormObject';
import { async } from 'q';
import http = require('http');
import { HttpResponse } from 'selenium-webdriver/http';
var Intercept = require('protractor-intercept');
var intercept = new Intercept(browser);

export class HomePageObject {
  searchFormObject : SearchFormObject = new SearchFormObject();
  switchOptions: ElementFinder = element.all(by.css("div[id$=switch-display]")).first();
  switchOneWayOption: ElementFinder = element.all(by.css("li[id$=switch-option-2]")).first();
  switchMultiCityOption: ElementFinder = element.all(by.css("li[id$=switch-option-3]")).first();
  switchRoundTripOption: ElementFinder = element.all(by.css("li[id$=switch-option-1]")).first();
  travelersGrid: ElementFinder = element.all(by.className("Flights-Search-StyleJamFlightTravelerDropdown")).first();
  addAdultButton: ElementFinder = element(by.css("div[id$='travelersAboveForm-adults'] .incrementor-js"));
  passengerErrorText: ElementFinder = element(by.css("div[id$=travelersAboveForm-errorMessage]"));
  originInput: ElementFinder = element.all(by.name('origin')).first();
  originSelect: ElementFinder = element.all(by.css("[class='flight-smarty'] li")).first();
  destinationInput: ElementFinder = element.all(by.name('destination')).first();
  destinationSelect: ElementFinder = (element.all(by.css('div[id$="destination-airport-smartbox-dropdown"')).first()).all(by.tagName('li')).first();
  passengerChildInput: ElementFinder = element(by.css("div[id$='travelersAboveForm-child'] .incrementor-js"));
  departureDateInput: ElementFinder = element.all(by.css("div[id$='depart-input']")).first();
  returnDateInput: ElementFinder = element(by.css("div[id$='return-input']"));
  searchButton: ElementFinder = element.all(by.css("button[aria-label='Search flights']")).first();
  checkbox: ElementFinder = element(by.css("button[aria-label='Disable results comparison for this search']"));
  returnDateText: ElementFinder = element.all(by.css("div[id$=dateRangeInput-display-end]")).first();
  multiCitiesOptions: ElementFinder = element.all(by.css("div[id$=origin1-airport-display]")).first();
  EC = protractor.ExpectedConditions;

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

  addAdultPassengers(adult: number) {
		this.searchFormObject.waitUntillElementAppears(this.travelersGrid);
		this.travelersGrid.click();
		this.searchFormObject.waitUntillElementAppears(this.addAdultButton);
		for(let i: number = 1; i < adult; i++) {
			this.addAdultButton.click();
		}
	}

	addChildPassengers(child: number): void {
		this.searchFormObject.waitUntillElementAppears(this.passengerChildInput);
		for(let i: number = 0; i < child; i++) {
			this.passengerChildInput.click();
		}
	}

	async getAdultsLimitMessage(): Promise<string> {
		await this.searchFormObject.waitUntillElementAppears(this.passengerErrorText);
		return this.passengerErrorText.getText();;
	}

	async setDeparture(departure: string) {
		this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureField);
		this.searchFormObject.departureField.click();
		this.searchFormObject.waitUntillElementAppears(this.originInput);
		this.originInput.sendKeys(Key.BACK_SPACE);
    this.originInput.sendKeys(Key.BACK_SPACE);
    this.originInput.sendKeys(departure);
    await this.searchFormObject.waitUntillElementAppears(this.originSelect);
		this.originSelect.click();
	}

	async setDestination(destination: string) {
    this.searchFormObject.waitUntillElementAppears(this.searchFormObject.destinationField);
		this.searchFormObject.destinationField.click();
		this.searchFormObject.waitUntillElementAppears(this.destinationInput);
		this.destinationInput.sendKeys(Key.BACK_SPACE);
		this.destinationInput.sendKeys(Key.BACK_SPACE);
    await this.destinationInput.sendKeys(destination);
    // intercept.addListener();
    // make events to get its requests
    // intercept.getRequests().then(function(reqs) {
    //make some assertions about what happened here
    // });
		await this.searchFormObject.waitUntillElementAppears(this.destinationSelect);
    this.destinationSelect.click();
  }

  async getChildPassenger(): Promise<string> {
    return await element(by.css('div[id$="travelersAboveForm-child"]')).getAttribute("aria-valuenow");
  }

  fillDatesDeparture(): void {
    this.searchFormObject.waitUntillElementAppears(this.searchFormObject.departureDateField);
    this.searchFormObject.departureDateField.click();
    this.searchFormObject.waitUntillElementAppears(this.departureDateInput);
    this.departureDateInput.click();
    this.departureDateInput.clear();
    this.departureDateInput.sendKeys(this.setTripDates(3));
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
    if (todaysDate.getDate() < 10) {
      dd = "0" + dd;
    }
    if(mm < '10') {
      mm = "0" + mm;
    }
    return (mm + "/" + dd + "/" + yyyy);
  }

  async uncheckAllCheckBox() {
    await this.searchFormObject.waitUntillElementAppears(this.checkbox);
    await this.checkbox.click();
  }
}
