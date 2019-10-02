import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";
import { Key } from "selenium-webdriver";
import { waitUntilInteractive } from "../../../../utils/browser.utils";
import { FlightSelector } from "../../../../core/elements/selectors/flightSelector";
import { FlightType } from "../../../../core/elements/types/flightType";

export class FlightSelectorKayak implements FlightSelector {
  constructor(readonly leg: number, readonly type: FlightType) {
  }
  
  async setText(text: string): Promise<void> {
    await this.makeInputInteractive();
    const input = this.getInputElement();
    await input.sendKeys(Key.BACK_SPACE);
    await input.sendKeys(text);
    await browser.wait(EC.textToBePresentInElementValue(input, text));
    return input.sendKeys(Key.ESCAPE)
  }
  
  async getDisplayText(): Promise<string> {
    return element(by.css(`div[id$='-${this.type}${this.leg}-airport-display']`)).getText();
  }
  
  async makeInputInteractive(): Promise<void> {
    const display = element(by.css(`div[id$='-${this.type}${this.leg}-airport-display']`));
    await waitUntilInteractive(display);
    display.click();
    
    await waitUntilInteractive(this.getInputElement());
  }
  
  getInputElement(): ElementFinder {
    return element(by.css(`input[name='${this.type}${this.leg}']`))
  }
  
}
