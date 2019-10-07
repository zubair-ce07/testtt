import { $, browser, ElementFinder, ExpectedConditions as EC, Key } from "protractor";
import { Destination } from "../../../../elements/input/destination";
import { waitUntilInteractive } from "../../../../utils/specs.utils";

export class DestinationKayak implements Destination {
  async type(text: string): Promise<void> {
    await this.showInput();
    
    const input = this.getInputElement();
    await input.sendKeys(Key.BACK_SPACE);
    await input.sendKeys(text);
    await browser.wait(EC.textToBePresentInElementValue(input, text));
    
    await this.hideInput();
  }
  
  async getDisplayText(): Promise<string> {
    return this.getInputContainer().getText();
  }
  
  private async showInput(): Promise<void> {
    const trigger = this.getInputContainer();
    const input = this.getInputElement();
    await trigger.click();
    await waitUntilInteractive(input);
  }
  
  private getInputContainer(): ElementFinder {
    return $(`div[id$='location-display-inner']`);
  }
  
  private async hideInput() {
    const input = this.getInputElement();
    await input.sendKeys(Key.ESCAPE);
    await browser.wait(EC.invisibilityOf(input));
  }
  
  private getInputElement(): ElementFinder {
    return $(`input[id$='location']`);
  }
}
