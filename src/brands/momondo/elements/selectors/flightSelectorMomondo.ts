import { browser, by, element, ElementFinder, ExpectedConditions as EC, Key } from "protractor";
import { waitUntilInteractive } from "../../../../utils/browser.utils";
import { FlightSelector } from "../../../../core/elements/selectors/flightSelector";
import { FlightType } from "../../../../core/elements/types/flightType";

export class FlightSelectorMomondo implements FlightSelector {
  constructor(readonly leg: number, readonly type: FlightType) {
  }
  
  async getDisplayText(): Promise<string> {
    return element(by.css(`input[name='${this.type}${this.leg}']`)).getAttribute('value');
  }
  
  async setText(text: string): Promise<void> {
    const input = await this.getInputElement();
    
    await waitUntilInteractive(input);
    await input.click();
    await waitUntilInteractive(input);
    
    await input.sendKeys(Key.BACK_SPACE);
    await input.sendKeys(text);
    await browser.wait(EC.textToBePresentInElementValue(input, text));
    await input.sendKeys(Key.ESCAPE);
  }
  
  async getInputElement(): Promise<ElementFinder> {
    const input = element(by.css(`input[id$='-${this.type}${this.leg}']`));
    const inputIsPresent = await input.isPresent();
    return inputIsPresent ? input : element(by.css(`input[id$='-${this.type}${this.leg}-airport']`))
  }
  
}
