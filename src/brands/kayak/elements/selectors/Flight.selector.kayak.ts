import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";
import { Key } from "selenium-webdriver";
import { FlightSelector } from "../../../../core/elements";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class FlightSelectorKayak implements FlightSelector {
  constructor(readonly leg: number) {
  }
  
  setOrigin(text: string): Promise<void> {
    return this.set('origin', text)
  }
  
  setDestination(text: string): Promise<void> {
    return this.set('destination', text)
  }
  
  async getDisplayText(type: 'origin' | 'destination'): Promise<string> {
    return element(by.css(`div[id$='-${type}${this.leg}-airport-display']`)).getText();
  }
  
  async set(type: string, text: string): Promise<void> {
    await this.makeInputInteractive(type);
    const input = this.getInputElement(type);
    await input.sendKeys(Key.BACK_SPACE);
    await input.sendKeys(text);
    await browser.wait(EC.textToBePresentInElementValue(input, text));
    return input.sendKeys(Key.ESCAPE)
  }
  
  async makeInputInteractive(type: string): Promise<void> {
    const display = element(by.css(`div[id$='-${type}${this.leg}-airport-display']`));
    await waitUntilInteractive(display);
    display.click();
    
    await waitUntilInteractive(this.getInputElement(type));
  }
  
  getInputElement(type: string): ElementFinder {
    return element(by.css(`input[name='${type}${this.leg}']`))
  }
  
}
