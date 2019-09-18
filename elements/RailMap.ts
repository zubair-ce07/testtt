import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from "protractor";


export class RailMap {
  show(): void {
    const map = element(by.className('Hotels-Results-Filters-HotelFilterList'))
      .element(by.className('Common-Results-MapToggle'));
    
    browser.wait(EC.visibilityOf(map));
    browser.wait(EC.elementToBeClickable(map));
    
    map.click();
    
    const mapContainer = this.getContainer();
    browser.wait(EC.presenceOf(mapContainer));
    browser.wait(EC.visibilityOf(mapContainer));
  }
  
  getContainer(): ElementFinder {
    return element(by.className('rail-map-container')).element(by.className('gm-style'))
  }
  
  hide(): void {
    const map = element(by.className('Hotels-Results-Filters-HorizontalHotelFilterList'))
      .element(by.className('Common-Results-MapToggle'));
    
    browser.wait(EC.visibilityOf(map));
    browser.wait(EC.elementToBeClickable(map));
    
    map.click();
    
    const mapContainer = this.getContainer();
    browser.wait(EC.invisibilityOf(mapContainer));
  }
  
  getMarkers(): ElementArrayFinder {
    return element(by.className('Hotels-Results-HotelRightRailMap'))
      .element(by.className(`gm-style`))
      .all(by.className('hotel-marker'));
  }
}
