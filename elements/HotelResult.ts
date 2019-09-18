import { browser, by, element, ElementFinder, ExpectedConditions as EC } from 'protractor';
import { MapMarker } from "./MapMarker";

export class HotelResult {
  constructor(readonly elm: ElementFinder) {
  }
  
  static async findFromMapMarker(marker: MapMarker) {
    const markerId = await marker.elm.getAttribute('id');
    const [ignore, id] = markerId.split('-');
    return new HotelResult(element(by.id(id)));
  }
  
  openDetailsWrapper() {
    this.elm.click();
    const wrapper = this.getDetailsWrapper();
    browser.wait(EC.presenceOf(wrapper));
    browser.wait(EC.visibilityOf(wrapper));
  }
  
  isDetailsWrapperDisplayed() {
    return this.getDetailsWrapper().isDisplayed()
  }
  
  getDetailsWrapper() {
    return this.elm.element(by.css(`div[id$='-detailsWrapper']`))
  }
  
  switchToTab(tab: 'Details' | 'Map' | 'Reviews' | 'Rates' | 'Overview') {
    tab = tab === 'Details' ? 'Overview' : tab;
    
    const tabToSwitch = this.elm
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab.toLowerCase()}']`));
    
    browser.wait(EC.presenceOf(tabToSwitch));
    browser.wait(EC.visibilityOf(tabToSwitch));
    browser.wait(EC.elementToBeClickable(tabToSwitch));
    tabToSwitch.click();
  }
  
  async closeDetailsWrapper() {
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
  
  getHotelImages() {
    return this.getTabContainer('Details')
      .element(by.className('col-photos'))
      .all(by.tagName('img'));
  }
  
  getHotelMap() {
    return this.getTabContainer('Map').element(by.className('map'));
  }
  
  getHotelReviews() {
    return this.getTabContainer('Reviews').element(by.className('Hotels-Results-InlineReviews'))
  }
  
  getHotelRates() {
    return this.getTabContainer('Rates').element(by.className('Hotels-Results-HotelRoomTypeRatesTable'))
  }
  
  getTabContainer(tab: 'Details' | 'Map' | 'Reviews' | 'Rates' | 'Overview') {
    tab = tab === 'Details' ? 'Overview' : tab;
    
    return this.elm
      .element(by.className(`Hotels-Results-InlineDetailTabs`))
      .element(by.css(`div[id$='-${tab.toLowerCase()}Container']`))
  }
  
  viewDeal() {
    return this.elm.element(by.css(`button[id$='-booking-bookButton']`)).click();
  }
}
