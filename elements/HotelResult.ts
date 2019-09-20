import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from 'protractor';
import { MapMarker } from "./MapMarker";
import { TabType } from "./TabType";

export class HotelResult {
  constructor(readonly container: ElementFinder) {
  }
  
  static async findFromMapMarker(marker: MapMarker): Promise<HotelResult> {
    const placeholder = element(by.className('Hotels-Results-HotelResultItemPlaceholder'));
    browser.wait(EC.invisibilityOf(placeholder));
  
    const markerId = await marker.marker.getAttribute('id');
    const [ignore, id] = markerId.split('-');
    const hotelResultContainer = element(by.id(id));
  
    browser.wait(EC.presenceOf(hotelResultContainer));
    browser.wait(EC.visibilityOf(hotelResultContainer));
    browser.wait(EC.elementToBeClickable(hotelResultContainer));
  
    return new HotelResult(hotelResultContainer);
  }
  
  openTabs(): void {
    this.container.click();
    const wrapper = this.getTabsContainer();
    browser.wait(EC.presenceOf(wrapper));
    browser.wait(EC.visibilityOf(wrapper));
  }
  
  switchToTab(tab: TabType): void {
    const tabToSwitch = this.container
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab}']`));
    
    browser.wait(EC.presenceOf(tabToSwitch));
    browser.wait(EC.visibilityOf(tabToSwitch));
    browser.wait(EC.elementToBeClickable(tabToSwitch));
    tabToSwitch.click();
    
    const tabContainer = this.getTabContainer(tab);
    browser.wait(EC.presenceOf(tabContainer));
    browser.wait(EC.visibilityOf(tabContainer));
  }
  
  async closeTabs(): Promise<void> {
    const isTabsContainerOpen = await this.getTabsContainer().isDisplayed();
    if (isTabsContainerOpen) {
      const closeButton = this.container
        .element(by.className(`Hotels-Results-InlineDetailTabs`))
        .element(by.css(`div[id$='-close']`));
      
      browser.wait(EC.presenceOf(closeButton));
      browser.wait(EC.visibilityOf(closeButton));
      browser.wait(EC.elementToBeClickable(closeButton));
      closeButton.click();
    }
  }
  
  getHotelImages(): ElementArrayFinder {
    const images = this.getTabContainer(TabType.DETAILS)
      .element(by.className('col-photos'))
      .all(by.tagName('img'));
  
    browser.wait(EC.presenceOf(images.first()));
  
    return images
  }
  
  getHotelMap(): ElementFinder {
    const map = this.getTabContainer(TabType.MAP).element(by.className('map'));
    browser.wait(EC.presenceOf(map));
    browser.wait(EC.visibilityOf(map));
    return map;
  }
  
  getHotelReviews(): ElementFinder {
    const reviews = this.getTabContainer(TabType.REVIEWS).element(by.className('Hotels-Results-InlineReviews'));
    browser.wait(EC.presenceOf(reviews));
    browser.wait(EC.visibilityOf(reviews));
    return reviews
  }
  
  getHotelRates(): ElementFinder {
    const rates = this.getTabContainer(TabType.RATES).element(by.className('Hotels-Results-HotelRoomTypeRatesTable'));
    browser.wait(EC.presenceOf(rates));
    browser.wait(EC.visibilityOf(rates));
    return rates
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
