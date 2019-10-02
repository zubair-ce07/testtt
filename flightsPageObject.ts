import {browser, $, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions} from 'protractor';

export class FlightsPageObject {
  departureField: ElementFinder = element(by.css('div[id$="origin-airport-display"]'));
  returnField: ElementFinder = element(by.css('div[id$="destination-airport-display"]'));
  departureDateText: ElementFinder = element(by.css("div[id$='dateRangeInput-display-start']"));
  returnDateText: ElementFinder = element(by.css("div[id$='dateRangeInput-display-end']"));
  cheapestPrice: ElementFinder = element(by.css("a[id$='price_aTab']"));
  bestPrice: ElementFinder = element(by.css("a[id$='bestflight_aTab']"));
  quickestPrice: ElementFinder = element(by.css("a[id$='duration_aTab']"));
  cheapestTime: ElementFinder = element(by.css("a[id$='price_aTab'] .js-duration"));
  bestTime: ElementFinder = element(by.css("a[id$='bestflight_aTab'] .js-duration"));
  quickestTime: ElementFinder = element(by.css("a[id$='duration_aTab'] .js-duration"));

  async getDeparture(): Promise<string> {
    return await this.departureField.getText();
  }

  async getDestination(): Promise<string> {
    return await this.returnField.getText();
  }

  getDepartureDate(): promise.Promise<string> {
    return this.departureDateText.getText();
  }

  getReturnDate(): promise.Promise<string> {
    return this.returnDateText.getText();
  }

  getTripDates(tripDaysNumber: number): string {
    const todaysDate = new Date();
    const weekdays: Array<String> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    todaysDate.setDate(todaysDate.getDate() + tripDaysNumber);
    const departureDayName = weekdays[todaysDate.getDay()];
    return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
  }

  async getCheapestPrice(): Promise<number> {
    return this.getPrice(await this.cheapestPrice.getText());
  }

  async getBestPrice(): Promise<number> {
    return this.getPrice(await this.bestPrice.getText());
  }

  async getQuickestPrice(): Promise<number> {
    return this.getPrice(await this.quickestPrice.getText());
  }
  
  getPrice(element: string): number {
    return parseFloat(element.match(/\$((?:\d|\,)*\.?\d+)/g)[0].split("$")[1]);
  }

  async getCheapestTime(): Promise<number> {
    return this.getTime(await this.cheapestTime.getText());
  }

  async getBestTime(): Promise<number> {
    return this.getTime(await this.bestTime.getText());
  }

  async getQuickestTime(): Promise<number> {
    return this.getTime(await this.quickestTime.getText());
  }
  
  getTime(time): number {
    const splitTime = time.replace("h", "").replace("m", "").split(" ");
    const timeInMiliSeconds = Number(splitTime[0])*3600 + Number(splitTime[1])*60;
    return timeInMiliSeconds;
  }
}
