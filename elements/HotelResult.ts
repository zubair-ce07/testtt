import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from 'protractor';
import { MapMarker } from "./MapMarker";
import { TabType } from "./TabType";
import { waitForElementToBeInteractive } from "../utils/browser.utils";

export class HotelResult {
  constructor(readonly container: ElementFinder) {
  }
  
  static async findFromMapMarker(marker: MapMarker): Promise<HotelResult> {
    const placeholder = element(by.className('Hotels-Results-HotelResultItemPlaceholder'));
    await browser.wait(EC.invisibilityOf(placeholder), 10 * 1000, 'Waiting for placeholder to hide');
    
    const markerId = await marker.marker.getAttribute('id');
    const [ignore, id] = markerId.split('-');
    const hotelResultContainer = element(by.id(id));
    await waitForElementToBeInteractive(hotelResultContainer);
    return new HotelResult(hotelResultContainer);
  }
  
  openTabs(): void {
    this.container.click();
  }
  
  switchToTab(tab: TabType): void {
    this.container
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab}']`))
      .click();
  }
  
  closeTabs(): void {
    this.container
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-close']`))
      .click();
  }
  
  getHotelImages(): ElementArrayFinder {
    const images = this.getTabContainer(TabType.DETAILS)
      .element(by.className('col-photos'))
      .all(by.tagName('img'));
  
    browser.wait(EC.presenceOf(images.first()));
  
    return images
  }
  
  getHotelMap(): ElementFinder {
    return this.getTabContainer(TabType.MAP).element(by.className('map'));
  }
  
  getHotelReviews(): ElementFinder {
    return this.getTabContainer(TabType.REVIEWS).element(by.className('Hotels-Results-InlineReviews'));
  }
  
  getHotelRates(): ElementFinder {
    return this.getTabContainer(TabType.RATES).element(by.className('Hotels-Results-HotelRoomTypeRatesTable'));
  }
  
  getTabsContainer(): ElementFinder {
    return this.container.element(by.css(`div[id$='-detailsWrapper']`))
  }
  
  getTabContainer(tab: TabType): ElementFinder {
    return this.container
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab}Container']`))
  }
  
  async viewDeal(): Promise<void> {
    return this.container.element(by.css(`button[id$='-booking-bookButton']`)).click();
  }
}
