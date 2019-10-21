import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions} from 'protractor';

export class SearchFormObject {
  departureDateField: ElementFinder = element.all(by.css('div[id$=dateRangeInput-display-start]')).first();
  returnDateField: ElementFinder = element.all(by.css('div[id$=dateRangeInput-display-end]')).first();
  departureField: ElementFinder = element.all(by.css('div[id$="origin-airport-display"]')).first();
  destinationField: ElementFinder = element.all(by.css('div[id$="destination-airport-display"]')).first();
  departureDateText: ElementFinder = element(by.css("div[id$='dateRangeInput-display-start']"));

  async getDepartureText(): Promise<string> {
    return await this.departureField.getText();
  }

  async getDestinationText(): Promise<string> {
    return await this.destinationField.getText();
  }

  getDepartureDateText(): promise.Promise<string> {
    return this.departureDateText.getText();
  }

  getReturnDateText(): promise.Promise<string> {
    return this.returnDateField.getText();
  }

  getDepartureDisplay(): ElementFinder {
    return this.departureField;
  }

  getDestinationDisplay(): ElementFinder {
    return this.destinationField;
  }

  departureDateFieldDisplay(): ElementFinder {
    return this.departureDateField;
  }

  returnDateFieldDisplay(): ElementFinder {
    return this.returnDateField;
  }

  async waitUntillElementAppears(element: any): Promise<void> {
    let until: ProtractorExpectedConditions = await protractor.ExpectedConditions; 
    await browser.wait(
    until.visibilityOf(element),
    4000, `${element} not appeared in expected time`)
  }

  async waitUntillElementDisappear(element: any): Promise<void> {
    let until: ProtractorExpectedConditions = await protractor.ExpectedConditions; 
    await browser.wait(
    until.invisibilityOf(element),
    4000, `${element} not disappeared in expected time`)
  }
}
