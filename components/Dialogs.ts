import { browser, by, element, ExpectedConditions } from "protractor";

export class PriceAlertDialog {
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