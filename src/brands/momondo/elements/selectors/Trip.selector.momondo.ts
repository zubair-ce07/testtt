import { browser, by, element, ExpectedConditions as EC } from "protractor";
import { TripSelector, TripType } from "../../../../core/elements";

export class TripSelectorMomondo implements TripSelector {
  async getCurrentTripType(): Promise<string> {
    const display = element(by.css(`div[id$='switch-display-status']`));
    const isDisplayPresent = await display.isPresent();
    
    if (isDisplayPresent) {
      return display.getAttribute('data-value')
    }
    
    return element(by.className(`r9-radiobuttonset-label-checked`)).getAttribute('title')
      .then(title => title.replace('-', '').toLowerCase())
  }
  
  async select(type: TripType): Promise<void> {
    let label = element(by.className('Flights-Search-FlightSearchForm'))
      .element(by.css(`label[id$='-${type}-label']`));
    
    const present = await label.isPresent();
    if (!present) {
      const displaySwitchContainer = element(by.className(`Flights-Search-StyleJamFlightSearchForm`));
      label = displaySwitchContainer.element(by.css(`div[id$='-switch-display']`));
      label.click();
      label = element(by.css(`ul[id$='-switch-list']`)).element(by.css(`li[data-value='${type}']`))
    }
    
    browser.wait(EC.visibilityOf(label));
    
    return label.click()
  }
  
}
