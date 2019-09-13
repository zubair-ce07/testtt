import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";

export class Trip {
  constructor(readonly id: string) {
  }
  
  getDialog(): ElementFinder {
    return element(by.id(`${this.id}-switch-display`))
  }
  
  getDialogWindow(): ElementFinder {
    return element(by.id(`${this.id}-switch-content`))
  }
  
  async select(type: TripType) {
    const dialog = this.getDialog();
    const dialogWindow = this.getDialogWindow();
    
    browser.wait(EC.elementToBeClickable(dialog));
    
    await dialog.click();
    browser.wait(EC.visibilityOf(dialogWindow));
    browser.wait(EC.elementToBeClickable(dialogWindow));
    
    const elm = element(by.id(`${this.id}-switch-option-${type}`));
    browser.wait(EC.elementToBeClickable(elm));
    await elm.click();
    
    await browser.wait(EC.invisibilityOf(dialogWindow))
  }
  
  value() {
    const elm = element(by.id(`${this.id}-switch-display-status`));
    browser.wait(EC.visibilityOf(elm));
    return elm.getText()
  }
}

export enum TripType {
  RoundTrip = 1,
  OneWay = 2,
  MultiCity = 3,
}