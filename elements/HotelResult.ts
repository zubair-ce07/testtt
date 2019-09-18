import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from 'protractor';
import { MapMarker } from "./MapMarker";

export class HotelResult {
  constructor(readonly elm: ElementFinder) {
  }
  
  static async findFromMapMarker(marker: MapMarker): Promise<HotelResult> {
    const placeholder = element(by.className('Hotels-Results-HotelResultItemPlaceholder'));
    browser.wait(EC.invisibilityOf(placeholder));
    
    const markerId = await marker.elm.getAttribute('id');
    const [ignore, id] = markerId.split('-');
    const $elm = element(by.id(id));
  
    browser.wait(EC.presenceOf($elm));
    browser.wait(EC.visibilityOf($elm));
    browser.wait(EC.elementToBeClickable($elm));
  
    return new HotelResult($elm);
  }
  
  openTabs(): void {
    this.elm.click();
    const wrapper = this.getTabsContainer();
    browser.wait(EC.presenceOf(wrapper));
    browser.wait(EC.visibilityOf(wrapper));
  }
  
  switchToTab(tab: 'Details' | 'Map' | 'Reviews' | 'Rates' | 'Overview'): void {
    tab = tab === 'Details' ? 'Overview' : tab;
    
    const tabToSwitch = this.elm
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab.toLowerCase()}']`));
    
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
      const closeButton = this.elm
        .element(by.className(`Hotels-Results-InlineDetailTabs`))
        .element(by.css(`div[id$='-close']`));
      
      browser.wait(EC.presenceOf(closeButton));
      browser.wait(EC.visibilityOf(closeButton));
      browser.wait(EC.elementToBeClickable(closeButton));
      closeButton.click();
    }
  }
  
  getHotelImages(): ElementArrayFinder {
    return this.getTabContainer('Details')
      .element(by.className('col-photos'))
      .all(by.tagName('img'));
  }
  
  getHotelMap(): ElementFinder {
    const map = this.getTabContainer('Map').element(by.className('map'));
    browser.wait(EC.presenceOf(map));
    browser.wait(EC.visibilityOf(map));
    return map;
  }
  
  getHotelReviews(): ElementFinder {
    const reviews = this.getTabContainer('Reviews').element(by.className('Hotels-Results-InlineReviews'));
    browser.wait(EC.presenceOf(reviews));
    browser.wait(EC.visibilityOf(reviews));
    return reviews
  }
  
  getHotelRates(): ElementFinder {
    const rates = this.getTabContainer('Rates').element(by.className('Hotels-Results-HotelRoomTypeRatesTable'));
    browser.wait(EC.presenceOf(rates));
    browser.wait(EC.visibilityOf(rates));
    return rates
  }
  
  getTabsContainer(): ElementFinder {
    return this.elm.element(by.css(`div[id$='-detailsWrapper']`))
  }
  
  getTabContainer(tab: 'Details' | 'Map' | 'Reviews' | 'Rates' | 'Overview'): ElementFinder {
    tab = tab === 'Details' ? 'Overview' : tab;
    
    return this.elm
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab.toLowerCase()}Container']`))
  }
  
  async viewDeal(): Promise<void> {
    return this.elm.element(by.css(`button[id$='-booking-bookButton']`)).click();
  }
}
