import { by, element, ElementFinder } from "protractor"
import { waitForElementToBeInteractive } from "../utils/browser.utils";

export class Destination {
  async type(text: string): Promise<void> {
    await this.makeInputFieldVisible();
    return this.getInputField().sendKeys(text);
  }
  
  getDisplayField(): ElementFinder {
    return element.all(by.css(`div[id$='-location-display']`)).first();
  }
  
  getInputField(): ElementFinder {
    return element.all(by.css(`input[id$='-location']`)).first();
  }
  
  async selectSearchResult(index: number): Promise<void> {
    const result = this.getSearchResultsElement().all(by.tagName('li')).get(index);
    await waitForElementToBeInteractive(result);
    result.click();
  }
  
  getSearchResultsElement(): ElementFinder {
    return element.all(by.css(`div[id$='-location-smartbox-dropdown']`)).first();
  }
  
  private async makeInputFieldVisible() {
    const inputField = this.getInputField();
    const isInputFieldDisplayed = await inputField.isDisplayed();
    if (!isInputFieldDisplayed) {
      this.getDisplayField().click();
      await waitForElementToBeInteractive(inputField);
    }
  }
}
