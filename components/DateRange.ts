import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";

export class DateRange {
  constructor(readonly id: string) {
  }
  
  getDialog(): ElementFinder {
    return element(by.id(`${this.id}-dateRangeInput-display`));
  }
  
  getDialogWindow(): ElementFinder {
    return element(by.id(`${this.id}-dateRangeInput-overlay-window`))
  }
  
  async openDialogWindow() {
    const dialog = this.getDialog();
    const content = this.getDialogWindow();
    browser.wait(EC.visibilityOf(dialog));
    browser.wait(EC.elementToBeClickable(dialog));
    await dialog.click();
    browser.wait(EC.visibilityOf(content));
  }
  
  async selectDate(start: Date, end: Date) {
    browser.wait(EC.visibilityOf(element(by.id(`${this.id}-dateRangeInput-overlay-window`))));
    
    {
      const elm = element(by.css(`div[data-val="${start.getTime()}"]`));
      await browser.wait(EC.visibilityOf(elm));
      await browser.wait(EC.elementToBeClickable(elm));
      await elm.click();
    }
    
    {
      const elm = element(by.css(`div[data-val="${end.getTime()}"]`));
      await browser.wait(EC.visibilityOf(elm));
      await browser.wait(EC.elementToBeClickable(elm));
      await elm.click();
    }
    
    browser.wait(EC.invisibilityOf(element(by.id(`${this.id}-dateRangeInput-overlay-content`))));
  }
  
  getDepartureDateDisplayValue() {
    const elm = element(by.id(`${this.id}-dateRangeInput-display-start-inner`));
    browser.wait(EC.visibilityOf(elm));
    return elm.getText();
  }
  
  getReturnDateDisplayValue() {
    const elm = element(by.id(`${this.id}-dateRangeInput-display-end-inner`));
    browser.wait(EC.visibilityOf(elm));
    return elm.getText();
  }
  
}