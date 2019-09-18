import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from 'protractor';
import { MapMarker } from "./MapMarker";

export class HotelResult {
  constructor(readonly elm: ElementFinder) {
  }
  
  static async findFromMapMarker(marker: MapMarker): Promise<HotelResult> {
    const markerId = await marker.elm.getAttribute('id');
    const [ignore, id] = markerId.split('-');
    return new HotelResult(element(by.id(id)));
  }
  
  openDetailsWrapper(): void {
    this.elm.click();
    const wrapper = this.getDetailsWrapper();
    browser.wait(EC.presenceOf(wrapper));
    browser.wait(EC.visibilityOf(wrapper));
  }
  
  async isDetailsWrapperDisplayed(): Promise<boolean> {
    return this.getDetailsWrapper().isDisplayed()
  }
  
  getDetailsWrapper(): ElementFinder {
    return this.elm.element(by.css(`div[id$='-detailsWrapper']`))
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
  }
  
  async closeDetailsWrapper(): Promise<void> {
    const isWrapperOpen = await this.isDetailsWrapperDisplayed();
    if (isWrapperOpen) {
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
    return this.getTabContainer('Map').element(by.className('map'));
  }
  
  getHotelReviews(): ElementFinder {
    return this.getTabContainer('Reviews').element(by.className('Hotels-Results-InlineReviews'))
  }
  
  getHotelRates(): ElementFinder {
    return this.getTabContainer('Rates').element(by.className('Hotels-Results-HotelRoomTypeRatesTable'))
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
