import { browser, by, element, ElementFinder, ExpectedConditions as EC, Key } from "protractor";

export class Passengers {
  constructor(readonly selector: string) {
  }
  
  getDialog(): ElementFinder {
    return element(by.id(`${this.selector}-dialog-trigger`))
  }
  
  getDialogWindow(): ElementFinder {
    return element(by.id(`${this.selector}-dialog_content`));
  }
  
  async openDialogWindow() {
    const dialog = this.getDialog();
    browser.wait(EC.visibilityOf(dialog));
    browser.wait(EC.elementToBeClickable(dialog));
    
    await dialog.click();
    
    browser.wait(EC.visibilityOf(this.getDialogWindow()));
    browser.wait(EC.elementToBeClickable(this.getDialogWindow()));
  }
  
  async closeDialogWindow() {
    const container = this.getDialog();
    browser.wait(EC.elementToBeClickable(container));
    await container.sendKeys(Key.ESCAPE);
    browser.wait(EC.invisibilityOf(this.getDialogWindow()));
  }
  
  async set(passenger: PassengerType | string, value: number) {
    await this.openDialogWindow();
    const total = await this.count(passenger).then(Number);
    
    if (total > value) {
      await this.decrement(passenger, total - value)
    } else {
      await this.increment(passenger, value - total)
    }
    
    await this.closeDialogWindow();
  }
  
  async increment(type: PassengerType | string, count: number) {
    const button = this.findButton(type, 'increment');
    
    for (let i = 0; i < count; i++) {
      browser.wait(EC.visibilityOf(button));
      browser.wait(EC.elementToBeClickable(button));
      await button.click();
    }
  }
  
  async decrement(type: PassengerType | string, count: number) {
    const button = this.findButton(type, 'decrement');
    for (let i = 0; i < count; i++) {
      browser.wait(EC.visibilityOf(button));
      browser.wait(EC.elementToBeClickable(button));
      await button.click();
    }
  }
  
  errorMessage() {
    const elm = element(by.id(`${this.selector}-errorMessage`));
    browser.wait(EC.visibilityOf(elm));
    return elm.getText()
  }
  
  count(passenger: PassengerType | string) {
    const elm = element(by.id(`${this.selector}-${passenger}-input`));
    browser.wait(EC.visibilityOf(elm));
    return elm.getAttribute('value')
  }
  
  async value() {
    return element.all(by.id(`${this.selector}`))
      .first().all(by.className('js-label'))
      .first().getAttribute('innerHTML')
  }
  
  private findButton(type: string, action: 'increment' | 'decrement') {
    const id = by.id(`${this.selector}-${type}`);
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