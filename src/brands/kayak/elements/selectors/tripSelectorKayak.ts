import { by, element, ElementFinder } from "protractor";
import { TripSelector } from "../../../../core/elements/selectors/tripSelector";
import { TripType } from "../../../../core/elements/types/tripType";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class TripSelectorKayak implements TripSelector {
  async getCurrentTripType(): Promise<string> {
    return element(by.css(`div[id$='-switch-display-status']`)).getAttribute('data-value');
  }
  
  async select(type: TripType): Promise<void> {
    this.getSwitchDisplay().click();
    const li = this.getSwitchList().element(by.css(`li[data-value='${type}']`));
    await waitUntilInteractive(li);
    await li.click();
  }
  
  getSwitchDisplay(): ElementFinder {
    return element(by.css(`div[id$='-switch-display']`))
  }
  
  getSwitchList(): ElementFinder {
    return element(by.css(`ul[id$='-switch-list'][aria-label='Choose a search type:']`))
  }
}
