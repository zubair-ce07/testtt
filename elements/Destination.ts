import { by, element, ElementFinder } from "protractor"
import { waitForElementToBeInteractive } from "../utils/browser.utils";

export class Destination {
  getDisplayField(): ElementFinder {
    return element.all(by.css(`div[id$='-location-display']`)).first();
  }
  
  getInputField(): ElementFinder {
    return element.all(by.css(`input[id$='-location']`)).first();
  }
  
  getSearchResultsElement(): ElementFinder {
    return element.all(by.css(`div[id$='-location-smartbox-dropdown']`)).first();
  }
  
  async selectSearchResult(index: number): Promise<void> {
    const result = this.getSearchResultsElement().all(by.tagName('li')).get(index);
    await waitForElementToBeInteractive(result);
    result.click();
  }
  
}
