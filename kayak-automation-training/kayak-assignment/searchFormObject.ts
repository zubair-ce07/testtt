import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions} from 'protractor';

export class SearchFormObject {
  departureDateField: ElementFinder = element.all(by.css('div[id$=dateRangeInput-display-start]')).first();
  returnDateField: ElementFinder = element.all(by.css('div[id$=dateRangeInput-display-end]')).first();
  departureField: ElementFinder = element.all(by.css('div[id$="origin-airport-display"]')).first();
  destinationField: ElementFinder = element.all(by.css('div[id$="destination-airport-display"]')).first();
  departureText: ElementFinder = element.all(by.css('div[id$="origin-airport-display-multi-container"]')).first();
  destinationText: ElementFinder = element.all(by.css('div[id$="destination-airport-display-multi-container"]')).first();
  passengerAdultText: ElementFinder = element(by.css('div[id$="travelersAboveForm-adults"]'));
  until: ProtractorExpectedConditions = protractor.ExpectedConditions;
  EC = protractor.ExpectedConditions;

  async waitUntillElementAppears(element: any): Promise<void> {
    await browser.wait(this.EC.visibilityOf(element), 5000)
  }

  async waitUntillElementDisappears(element: any): Promise<void> {
    await browser.wait(
    this.EC.invisibilityOf(element),
    4000, `${element} not appeared in expected time`)
  }

  waitFortextPresentInElement (element: ElementFinder, text: string): void {
    browser.wait(this.EC.textToBePresentInElement(element, text), 30000);
  }

  async getDepartureValue(): Promise<string> {
    await this.waitUntillElementAppears(this.departureText);
    return await this.departureText.getText();
  }

  async getDestinationValue(): Promise<string> {
    await this.waitUntillElementAppears(this.destinationText);
    return await  this.destinationText.getText();
  }

  async getAdultPassengers(): Promise<string> {
    await this.waitUntillElementAppears(this.passengerAdultText);
    return await this.passengerAdultText.getAttribute("aria-valuenow");
  }

  getDepartureDate(): ElementFinder {
    return this.departureDateField;
  }

  getReturnDate(): promise.Promise<string> {
    return this.returnDateField.getText();
  }
}
