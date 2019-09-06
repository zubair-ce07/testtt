import { browser, by, element, ElementFinder, ExpectedConditions, Key }                 from "protractor";
import { waitForPageLoad }                                                              from "../utils/browser.util";
import { AirportSelector, CompareTo, DateRange, FlightFilterType, PassengerType, Trip } from "./Flights";

export class FlightsResultsPage {
  public form: SearchForm;
  public dialog: PriceAlertDialog;
  public header: FlightResultsHeader;
  
  constructor(private url: string) {
    this.dialog = new PriceAlertDialog();
    this.header = new FlightResultsHeader();
  }
  
  async load() {
    const url = await browser.getCurrentUrl();
    
    if (this.url !== url) {
      await browser.get(this.url);
      await browser.executeAsyncScript(waitForPageLoad());
    }
    
    await element(by.className('Flights-Search-FlightInlineSearchForm'))
      .getAttribute('id')
      .then(id => {
        this.form = new SearchForm(id);
      });
    
    await Promise.all([
      this.form.load(),
      this.header.load(),
    ]);
    
    await this.dialog.load()
  }
}

class PriceAlertDialog {
  private id: string;
  
  async load() {
    const locator = by.className('Flights-Results-FlightPriceAlertDriveBy');
    
    return element(locator).isPresent()
      .then(present => {
        if (present) {
          return element(locator).getAttribute('id')
        }
      })
      .then(id => {
        this.id = id;
      })
  }
  
  get() {
    return element(by.id(this.id));
  }
  
  closeIfOpen() {
    if (this.id !== null) {
      const elm = element(by.id(`${this.id}-dialog-close`));
      return elm.isPresent().then(isPresent => {
        if (isPresent) {
          browser.wait(ExpectedConditions.visibilityOf(elm));
          return elm.click();
        }
      })
    }
  }
}

class FlightResultsHeader {
  private id: string;
  
  async load() {
    browser.wait(ExpectedConditions.presenceOf(element(by.className('hideSubTitle'))));
    
    return element(by.className('Flights-Results-FlightSnackshotHeader')).getAttribute('id').then(id => {
      this.id = id;
    })
  }
  
  select(type: FlightFilterType) {
    return element(by.id(`${this.id}-${type}_aTab`)).click();
  }
  
  getCost(type: FlightFilterType) {
    return element.all(by.id(`${this.id}-${type}_aTab`))
      .first().all(by.className('js-price'))
      .first().getAttribute('innerHTML')
  }
  
  getDuration(type: FlightFilterType) {
    return element.all(by.id(`${this.id}-${type}_aTab`))
      .first().all(by.className('js-duration'))
      .first().getAttribute('innerHTML')
  }
  
}

class SearchForm {
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
  
  submit() {
    // qE6J-submit
    
    const elm = element(by.id(`${this.id}-submit`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    
    return element(by.id(`${this.id}-submit`)).click();
  }
  
  private async findSelectTripTypeId() {
    return element(by.id(this.id))
      .all(by.className('displaySwitch'))
      .all(by.tagName('div'))
      .first()
      .getAttribute('id')
  }
}

class Passengers {
  constructor(readonly id: string) {
  }
  
  get() {
    return element(by.id(`${this.id}-travellers`))
  }
  
  openDialog() {
    const elm = element(by.id(`${this.id}-travelers-dialog-trigger`));
    browser.wait(ExpectedConditions.elementToBeClickable(elm));
    return elm.click();
  }
  
  closeDialog() {
    browser.wait(ExpectedConditions.elementToBeClickable(this.get()));
    return this.get().sendKeys(Key.ESCAPE)
  }
  
  isDialogOpen() {
    return element(by.id(`${this.id}-travelers-dialog_content`)).isPresent()
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
    const elm = element(by.id(`${this.id}-travelers-errorMessage`));
    browser.wait(ExpectedConditions.visibilityOf(elm));
    return elm.getText()
  }
  
  count(passenger: PassengerType | string) {
    // dYIV-travelersAboveForm-{adults|...}-input
    const elm = element(by.id(`${this.id}-travelers-${passenger}-input`));
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
    
    return element.all(by.id(`${this.id}-travelers`))
      .first().all(by.className('js-label'))
      .first().getText()
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