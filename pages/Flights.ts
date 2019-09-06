import { browser, by, element, ElementFinder, ExpectedConditions, Key } from 'protractor';
import { waitForPageLoad }                                              from "../utils/browser.util";
import { FlightsResultsPage }                                           from "./FlightsResults";

export class LandingPage {
  public searchForm: SearchForm;
  
  async load() {
    await browser.get('https://www.kayak.com');
    await browser.executeAsyncScript(waitForPageLoad());
    
    await element(by.className('Base-Search-SearchForm')).getAttribute('id').then(id => {
      this.searchForm = new SearchForm(id);
    });
    
    return this.searchForm.load();
  }
}

export class SearchForm {
  public trip: Trip;
  public origin: AirportSelector;
  public destination: AirportSelector;
  public passengers: Passengers;
  public dateRange: DateRange;
  public compare: CompareTo;
  
  constructor(readonly id: string) {
    this.origin = new AirportSelector(id, 'origin');
    this.compare = new CompareTo(id);
    this.dateRange = new DateRange(id);
    this.passengers = new Passengers(id);
    this.destination = new AirportSelector(id, 'destination');
  }
  
  async load() {
    return this.findSelectTripTypeId().then(id => {
      this.trip = new Trip(id);
    })
  }
  
  get(): ElementFinder {
    return element(by.id(this.id))
  }
  
  async submit(): Promise<FlightsResultsPage> {
    const elm = element(by.id(`${this.id}-submit`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    
    return element(by.id(`${this.id}-submit`))
      .click()
      .then(async () => {
        return new FlightsResultsPage(await browser.getCurrentUrl());
      })
  }
  
  private async findSelectTripTypeId() {
    return element.all(by.id(this.id))
      .first().all(by.tagName('div'))
      .first().all(by.tagName('div'))
      .first().all(by.tagName('div'))
      .first().getAttribute('id')
  }
  
}

export class Trip {
  constructor(readonly id: string) {
  }
  
  get() {
    return element(by.id(`${this.id}-switch-display`))
  }
  
  select(type: TripType) {
    browser.wait(ExpectedConditions.elementToBeClickable(this.get()));
    
    return this.get().click().then(() => {
      const elm = element(by.id(`${this.id}-switch-option-${type}`));
      browser.wait(ExpectedConditions.elementToBeClickable(elm));
      return elm.click()
    })
  }
  
  /**
   * Returns selected trip type value
   */
  value() {
    const elm = element(by.id(`${this.id}-switch-display-status`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getText()
  }
}

export enum TripType {
  RoundTrip = 1,
  OneWay = 2,
  MultiCity = 3,
}

export class AirportSelector {
  constructor(readonly id: string, readonly airportType: 'origin' | 'destination') {
  }
  
  get() {
    return element(by.id(`${this.id}-${this.airportType}`))
  }
  
  clear() {
    const multi = this.getMultiContainer();
    return multi.isPresent().then(async yes => {
      if (yes) {
        const count = await multi.all(by.tagName('button')).count();
        
        if (count > 0) {
          await multi.all(by.tagName('button'))
            .each(button => button.click()) // remove all selected
            .then(() => {
              const elm = element(by.id(`${this.id}-${this.airportType}-airport`));
              browser.wait(ExpectedConditions.elementToBeClickable(elm));
              return elm.sendKeys(Key.ESCAPE)
            })
        }
      }
      
      return yes;
    })
  }
  
  type(location: string, clearPreviousInput = true) {
    const elm = element(by.id(`${this.id}-${this.airportType}-airport`));
    
    return Promise.resolve(clearPreviousInput ? this.clear() : false)
      .then(async () => {
        browser.wait(ExpectedConditions.elementToBeClickable(this.get()));
        await this.get().click();
        browser.wait(ExpectedConditions.visibilityOf(elm));
        browser.wait(ExpectedConditions.elementToBeClickable(elm));
        return elm.sendKeys(location);
      })
  }
  
  select(option: number) {
    // p_Ro-origin-airport-smartbox-dropdown
    browser.wait(ExpectedConditions.visibilityOf(element(by.id(`${this.id}-${this.airportType}-airport-smarty-content`))));
    const elm = element.all(by.id(`${this.id}-${this.airportType}-airport-smartbox-dropdown`))
      .first().all(by.tagName('li')).get(option - 1);
    
    browser.wait(ExpectedConditions.presenceOf(elm));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    
    return elm.click()
  }
  
  async getSearchResults(): Promise<Airport[]> {
    return element(by.id(`${this.id}-${this.airportType}-airport-smartbox-dropdown`))
      .all(by.tagName('li'))
      .then(async elements => {
        const airports = [];
        
        for (const element of elements) {
          const airport: string = await element.getText();
          let [location, name, code] = airport.split('\n');
          if (!code) {
            // sometimes name is undefined and contains ap-code
            code = name;
          }
          
          airports.push(new Airport(name, location, code));
        }
        
        return airports;
      })
    
  }
  
  async getSelectedValue() {
    const multi = this.getMultiContainer();
    return multi.isPresent().then(isPresent => {
      if (isPresent) {
        const elm = multi.all(by.className('js-selection-display')).first();
        browser.wait(ExpectedConditions.visibilityOf(elm));
        return elm.getText()
      } else {
        const elm = element(by.id(`${this.id}-${this.airportType}-airport`));
        return elm.getAttribute('value')
      }
    });
  }
  
  private getMultiContainer() {
    return element(by.id(`${this.id}-${this.airportType}-airport-display-multi-container`));
  }
}

class Passengers {
  constructor(readonly id: string) {
  }
  
  get() {
    return element(by.id(`${this.id}-travelersAboveForm-dialog-trigger`))
  }
  
  openDialog() {
    const elm = element(by.id(`${this.id}-travelersAboveForm-dialog-trigger`));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    return elm.click();
  }
  
  closeDialog() {
    browser.wait(ExpectedConditions.elementToBeClickable(this.get()));
    return this.get().sendKeys(Key.ESCAPE)
  }
  
  isDialogOpen() {
    return element(by.id(`${this.id}-travelersAboveForm-dialog_content`)).isPresent()
  }
  
  set(passenger: PassengerType | string, value: number) {
    return this.openDialog()
      .then(() => browser.sleep(1000))
      .then(() => this.count(passenger))
      .then(count => Number(count))
      .then(count => {
        if (count > value) {
          return this.decrement(passenger, count - value);
        } else {
          return this.increment(passenger, value - count)
        }
      })
      .then(() => {
        return this.closeDialog()
      })
  }
  
  increment(type: PassengerType | string, count: number) {
    const button = this.findButton(type, 'increment');
    browser.wait(ExpectedConditions.elementToBeClickable(button));
    for (let i = 0; i < count; i++) {
      button.click();
    }
  }
  
  decrement(type: PassengerType | string, count: number) {
    const button = this.findButton(type, 'decrement');
    browser.wait(ExpectedConditions.elementToBeClickable(button));
    for (let i = 0; i < count; i++) {
      button.click();
    }
  }
  
  errorMessage() {
    const elm = element(by.id(`${this.id}-travelersAboveForm-errorMessage`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getText()
  }
  
  count(passenger: PassengerType | string) {
    // dYIV-travelersAboveForm-{adults|...}-input
    const elm = element(by.id(`${this.id}-travelersAboveForm-${passenger}-input`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getAttribute('value')
  }
  
  async value() {
    // GuTL-travelers-dialog-trigger
    
    // main: VQKB-travelersAboveForm
    // const isAboveForm = await element(by.id(`${this.id}-travelersAboveForm`));
    // if (isAboveForm) {
    //   return element(by.id(`${this.id}`))
    //     .all(by.className('col-travelers'))
    //     .first().all(by.className('js-label'))
    //     .first()
    //     .getText();
    // } else {
    //   return element(by.id(`${this.id}-travelers`))
    //     .all(by.className('col-travelers'))
    //     .first().all(by.className('js-label'))
    //     .first()
    //     .getText();
    // }
    
    // return element(by.id(`${this.id}`))
    //   .all(by.className('col-travelers'))
    //   .first().all(by.className('js-label'))
    //   .first()
    //   .getText();
    
    return element.all(by.id(`${this.id}-travelersAboveForm`))
      .first().all(by.className('js-label'))
      .first().getAttribute('innerHTML')
  }
  
  async reset() {
    const passengers = [
      {type: PassengerType.Adults, value: 1},
      {type: PassengerType.Seniors, value: 0},
      {type: PassengerType.Child, value: 0},
      {type: PassengerType.Youth, value: 0},
      {type: PassengerType.SeatInfant, value: 0},
      {type: PassengerType.LapInfant, value: 0},
    ];
    return this.openDialog()
      .then(() => browser.sleep(1000))
      .then(async () => {
        for (const {type, value} of passengers) {
          const count: number = await this.count(type).then(Number);
          
          if (count > value) {
            this.decrement(type, count - value);
          } else {
            this.increment(type, value - count)
          }
        }
      })
      .then(() => {
        return this.closeDialog()
      })
    
  }
  
  private findButton(type: string, action: 'increment' | 'decrement') {
    // LNIb-travelersAboveForm-{adults|...}
    const id = by.id(`${this.id}-travelersAboveForm-${type}`);
    const idx = ['decrement', 'increment'].indexOf(action);
    
    return element.all(id)
      .first().all(by.tagName('div'))
      .first().all(by.tagName('button'))
      .get(idx);
  }
}

export enum PassengerType {
  Adults = 'adults',
  Seniors = 'seniors',
  Youth = 'youth',
  Child = 'child',
  SeatInfant = 'seatInfant',
  LapInfant = 'lapInfant',
}

export class CompareTo {
  constructor(readonly id: string) {
  }
  
  selectAll() {
    // qE6J-compareTo-allLink
    return element(by.id(`${this.id}-compareTo-allLink`)).click()
  }
  
  selectNone() {
    // qE6J-compareTo-noneLink
    const elm = element(by.id(`${this.id}-compareTo-noneLink`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    return elm.click()
  }
  
  selectOption(option: number) {
    return element.all(`${this.id}-compareTo-checkbox-row`)
      .first().getAttribute('innerHTML')
      .then(html => {
        console.log('compare', html);
      })
  }
  
}

export enum FlightFilterType {
  Cheapest = "price",
  Best = "bestflight",
  Quickest = "duration",
}

export class DateRange {
  constructor(readonly id: string) {
  }
  
  get() {
    // -dateRangeInput-overlay-window
    return element(by.id(`${this.id}-dateRangeInput-overlay-window`))
  }
  
  isOpen() {
    return element(by.id(`${this.id}-dateRangeInput-overlay-window`)).isDisplayed()
  }
  
  async selectDate(start: Date, end: Date) {
    console.log('selecting date');
    
    browser.wait(ExpectedConditions.visibilityOf(element(by.id(`${this.id}-dateRangeInput-overlay-window`))));
    
    {
      const elm = element(by.css(`div[data-val="${start.getTime()}"]`));
      await browser.wait(ExpectedConditions.visibilityOf(elm));
      await browser.wait(ExpectedConditions.elementToBeClickable(elm));
      await elm.click();
    }
    
    {
      const elm = element(by.css(`div[data-val="${end.getTime()}"]`));
      await browser.wait(ExpectedConditions.visibilityOf(elm));
      await browser.wait(ExpectedConditions.elementToBeClickable(elm));
      await elm.click();
    }
    
    console.log('waiting for close');
    browser.wait(ExpectedConditions.invisibilityOf(element(by.id(`${this.id}-dateRangeInput-overlay-content`))));
  }
  
  getDepartureDateDisplayValue() {
    // oQbJ-dateRangeInput-display-start-inner
    const elm = element(by.id(`${this.id}-dateRangeInput-display-start-inner`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getText();
  }
  
  getReturnDateDisplayValue() {
    // oQbJ-dateRangeInput-display-end-inner
    const elm = element(by.id(`${this.id}-dateRangeInput-display-end-inner`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getText();
  }
  
  open() {
    const elm = element(by.id(`${this.id}-dateRangeInput-display`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    return elm.click();
  }
  
  close() {
    return this.get().sendKeys(Key.ESCAPE);
    // return element(by.tagName('body')).sendKeys(Key.ESCAPE);
  }
  
}

export class Airport {
  constructor(
    readonly name: string,
    readonly location: string,
    readonly code: string,
  ) {
  }
}
