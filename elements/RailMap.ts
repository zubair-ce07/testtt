import { by, element, ElementArrayFinder, ElementFinder } from "protractor";
import { waitForElementToBeInteractive } from "../utils/browser.utils";

export class RailMap {
  async show(): Promise<void> {
    const showMap = element(by.className('Hotels-Results-Filters-HotelFilterList'))
      .element(by.className('Common-Results-MapToggle'));
    
    await waitForElementToBeInteractive(showMap);
    return showMap.click();
  }
  
  getContainer(): ElementFinder {
    return element(by.className('rail-map-container')).element(by.className('gm-style'))
  }
  
  async hide(): Promise<void> {
    const hideMap = element(by.className('Hotels-Results-Filters-HorizontalHotelFilterList'))
      .element(by.className('Common-Results-MapToggle'));
    
    await waitForElementToBeInteractive(hideMap);
    return hideMap.click();
  }
  
  getMarkers(): ElementArrayFinder {
    return element(by.className('Hotels-Results-HotelRightRailMap'))
      .element(by.className(`gm-style`))
      .all(by.className('hotel-marker'));
  }
}
