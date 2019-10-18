import {browser, $, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions} from 'protractor';
import { SearchFormObject } from './searchFormObject';

export class FlightsPageObject {
  searchFormObject: SearchFormObject = new SearchFormObject();
  cheapestPrice: ElementFinder = element(by.css("a[id$='price_aTab'] .js-price"));
  bestPrice: ElementFinder = element(by.css("a[id$='bestflight_aTab'] .js-price"));
  quickestPrice: ElementFinder = element(by.css("a[id$='duration_aTab'] .js-price"));
  cheapestTime: ElementFinder = element(by.css("a[id$='price_aTab'] .js-duration"));
  bestTime: ElementFinder = element(by.css("a[id$='bestflight_aTab'] .js-duration"));
  quickestTime: ElementFinder = element(by.css("a[id$='duration_aTab'] .js-duration"));
  EC = protractor.ExpectedConditions

  getTripDates(tripDaysNumber: number): string {
    const todaysDate = new Date();
    const weekdays: Array<String> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    todaysDate.setDate(todaysDate.getDate() + tripDaysNumber);
    const departureDayName = weekdays[todaysDate.getDay()];
    return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
  }

  async getCheapestPrice(): Promise<string> {
    browser.wait(this.EC.textToBePresentInElement(this.cheapestPrice, '$'), 8000);
    return (await this.cheapestPrice.getText()).toString().split("$")[1];
  }

  async getBestPrice(): Promise<string> {
    browser.wait(this.EC.textToBePresentInElement(this.bestPrice, '$'), 8000);
    return (await this.cheapestPrice.getText()).toString().split("$")[1];
  }

  async getQuickestPrice(): Promise<string> {
    browser.wait(this.EC.textToBePresentInElement(this.quickestPrice, '$'), 25000);
    return (await this.cheapestPrice.getText()).toString().split("$")[1];
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
