import { browser, by, element, ExpectedConditions as EC } from "protractor";

export class FlightCompare {
  constructor(readonly id: string) {
  }
  
  selectAll() {
    return element(by.id(`${this.id}-compareTo-allLink`)).click()
  }
  
  selectNone() {
    const elm = element(by.id(`${this.id}-compareTo-noneLink`));
    browser.wait(EC.presenceOf(elm), 1000, 'Waiting for element to be present');
    browser.wait(EC.visibilityOf(elm), 1000, 'Waiting for element to be visible');
    browser.wait(EC.elementToBeClickable(elm), 1000, 'Waiting for element to be clickable');
    return elm.click()
  }
  
}

export enum FlightFilters {
  Cheapest = 'price',
  Best = 'bestflight',
  Quickest = 'duration',
}

export class FlightResultsHeader {
  private id: string;
  
  async load() {
    browser.wait(EC.presenceOf(element(by.className('hideSubTitle'))));
    
    return element(by.className('Flights-Results-FlightSnackshotHeader')).getAttribute('id').then(id => {
      this.id = id;
    })
  }
  
  select(type: FlightFilters) {
    return element(by.id(`${this.id}-${type}_aTab`)).click();
  }
  
  getCost(type: FlightFilters) {
    return element.all(by.id(`${this.id}-${type}_aTab`))
      .first().all(by.className('js-price'))
      .first().getAttribute('innerHTML')
  }
  
  getDuration(type: FlightFilters) {
    return element.all(by.id(`${this.id}-${type}_aTab`))
      .first().all(by.className('js-duration'))
      .first().getAttribute('innerHTML')
  }
  
}