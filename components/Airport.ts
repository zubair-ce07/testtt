import { browser, by, element, ElementFinder, ExpectedConditions as EC, Key } from "protractor";

export class AirportSelector {
  private readonly selector: string;
  
  constructor(id: string, readonly airportType: 'origin' | 'destination') {
    this.selector = `${id}-${airportType}`
  }
  
  getDialog(): ElementFinder {
    return element(by.id(`${this.selector}`))
  }
  
  getDialogWindow(): ElementFinder {
    return element(by.id(`${this.selector}-airport-smarty-window`))
  }
  
  getMultiInputContainer() {
    return element(by.id(`${this.selector}-airport-display-multi-container`));
  }
  
  clear() {
    const multi = this.getMultiInputContainer();
    return multi.isPresent().then(async yes => {
      if (yes) {
        const count = await multi.all(by.tagName('button')).count();
        
        if (count > 0) {
          await multi.all(by.tagName('button')).each(button => button.click()); // remove all selected
          
          const elm = element(by.id(`${this.selector}-airport`));
          browser.wait(EC.elementToBeClickable(elm));
          return elm.sendKeys(Key.ESCAPE)
        }
      }
      
      return yes;
    })
  }
  
  async type(location: string, clearPreviousInput = true) {
    const input = element(by.id(`${this.selector}-airport`));
    const dialog = this.getDialog();
    const dialogWindow = this.getDialogWindow();
    
    if (clearPreviousInput) {
      await this.clear()
    }
    
    browser.wait(EC.visibilityOf(dialog));
    browser.wait(EC.elementToBeClickable(dialog));
    await dialog.click();
    
    browser.wait(EC.visibilityOf(dialogWindow));
    
    await input.clear();
    await input.sendKeys(location);
  }
  
  select(option: number) {
    browser.wait(EC.visibilityOf(element(by.id(`${this.selector}-airport-smarty-content`))));
    const elm = element.all(by.id(`${this.selector}-airport-smartbox-dropdown`))
      .first().all(by.tagName('li')).get(option - 1);
    
    browser.wait(EC.presenceOf(elm));
    browser.wait(EC.visibilityOf(elm));
    browser.wait(EC.elementToBeClickable(elm));
    
    return elm.click()
  }
  
  async getSearchResults(): Promise<Airport[]> {
    const elements = await element(by.id(`${this.selector}-airport-smartbox-dropdown`))
      .all(by.tagName('li'));
    
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
  }
  
  async getSelectedValue() {
    const multi = this.getMultiInputContainer();
    const isMultiInputContainer = await multi.isPresent();
    
    if (isMultiInputContainer) {
      const elm = multi.all(by.className('js-selection-display')).first();
      browser.wait(EC.visibilityOf(elm));
      return elm.getText()
    } else {
      const elm = element(by.id(`${this.selector}-airport-display-inner`));
      browser.wait(EC.visibilityOf(elm));
      return elm.getText()
    }
    
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