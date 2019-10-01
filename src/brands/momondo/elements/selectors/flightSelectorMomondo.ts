import { browser, by, element, ElementFinder, ExpectedConditions as EC, Key } from "protractor";
import { FlightSelector } from "../../../../core/elements/selectors/flightSelector";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class FlightSelectorMomondo implements FlightSelector {
  constructor(readonly leg: number) {
  }
  
  setDestination(text: string): Promise<void> {
    return this.set('destination', text);
  }
  
  setOrigin(text: string): Promise<void> {
    return this.set('origin', text);
  }
  
  async getDisplayText(type: 'origin' | 'destination'): Promise<string> {
    return element(by.css(`input[name='${type}${this.leg}']`)).getAttribute('value');
  }
  
  async set(type: string, text: string): Promise<void> {
    const input = await this.getInputElement(type);
    
    await waitUntilInteractive(input);
    await input.click();
    await waitUntilInteractive(input);
    
    await input.sendKeys(Key.BACK_SPACE);
    await input.sendKeys(text);
    await browser.wait(EC.textToBePresentInElementValue(input, text));
    await input.sendKeys(Key.ESCAPE);
  }
  
  async getInputElement(type: string): Promise<ElementFinder> {
    const input = element(by.css(`input[id$='-${type}${this.leg}']`));
    const inputIsPresent = await input.isPresent();
    return inputIsPresent ? input : element(by.css(`input[id$='-${type}${this.leg}-airport']`))
  }
  
}
