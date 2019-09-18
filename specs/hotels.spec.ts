import { browser } from "protractor";
import { expect, use } from "chai";
import chaiAsPromised from "chai-as-promised";
import { Kayak } from "../pages/Kayak";
import { Hotels } from "../pages/Hotels";
import { HotelsResults } from "../pages/HotelsResults";
import { MapMarker } from "../elements/MapMarker";
import { HotelResult } from "../elements/HotelResult";

use(chaiAsPromised);

describe('Kayak.com/hotels', () => {
  const Pages = {
    kayak: new Kayak(),
    hotels: new Hotels(),
    hotelsResults: new HotelsResults(),
  };
  
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(done)
  });
  
  it('should open kayak.com', async () => {
    const url = 'https://www.kayak.com';
    browser.get(url);
    expect(browser.getCurrentUrl()).eventually.to.contain(url);
  });
  
  it('should click "Hotels" on navigation bar', () => {
    Pages.kayak.navigation.to('hotels');
    const hotelsPage = Pages.hotels;
    expect(browser.getCurrentUrl()).eventually.to.equal('https://www.kayak.com/hotels');
    expect(hotelsPage.travellers.getDisplayText()).eventually.to.equal('1 room, 2 guests');
    expect(hotelsPage.dateRange.getStartDateElement().isPresent()).eventually.to.be.true;
    expect(hotelsPage.dateRange.getEndDateElement().isPresent()).eventually.to.be.true;
    expect(hotelsPage.destination.getDialog().isPresent()).eventually.to.be.true;
  });
  
  it('should load hotels results for search string BCN', async () => {
    const text = 'BCN';
    Pages.hotels.destination.type(text);
    Pages.hotels.destination.selectSearchResult(0);
    Pages.hotels.clickSearch();
    await Pages.hotelsResults.load();
    expect(Pages.hotelsResults.getSearchResults().count()).eventually.to.be.gte(5);
  });
  
  it('should open details of first search result', async () => {
    const resultsPage = Pages.hotelsResults;
    const searchResult = resultsPage.getSearchResult(0);
    searchResult.openDetailsWrapper();
    expect(searchResult.isDetailsWrapperDisplayed()).eventually.to.be.true;
    
    expect(searchResult.getHotelImages().count(), 'details tab should contain hotel images')
      .eventually.to.be.greaterThan(0);
  });
  
  it('should switch to "Map" tab', () => {
    const resultsPage = Pages.hotelsResults;
    const tab = 'Map';
    const searchResult = resultsPage.getSearchResult(0);
    searchResult.switchToTab(tab);
    expect(searchResult.getTabContainer(tab).isDisplayed()).eventually.to.be.true;
    expect(searchResult.getHotelMap().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Reviews" tab', async () => {
    const resultsPage = Pages.hotelsResults;
    const tab = 'Reviews';
    const searchResult = resultsPage.getSearchResult(0);
    searchResult.switchToTab(tab);
    expect(searchResult.getTabContainer(tab).isDisplayed()).eventually.to.be.true;
    expect(searchResult.getHotelReviews().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Rates" tab', async () => {
    const resultsPage = Pages.hotelsResults;
    const tab = 'Rates';
    const searchResult = resultsPage.getSearchResult(0);
    searchResult.openDetailsWrapper();
    searchResult.switchToTab(tab);
    expect(searchResult.getTabContainer(tab).isDisplayed()).eventually.to.be.true;
    expect(searchResult.getHotelRates().isDisplayed()).eventually.to.be.true;
  });
  
  it('should open "map view" ', () => {
    const resultsPage = Pages.hotelsResults;
    resultsPage.railMap.show();
    expect(resultsPage.railMap.getContainer().isDisplayed()).eventually.to.be.true;
    expect(resultsPage.getHorizontalFiltersContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should show map marker details when mouse hovered', async () => {
    const resultsPage = Pages.hotelsResults;
    
    const markers = resultsPage.railMap.getMarkers();
    const marker = new MapMarker(markers.last());
    await marker.hoverMouse();
    expect(marker.isSummaryCardDisplayed(), 'market details should show').eventually.to.be.true;
  });
  
  it('should open hotel card when clicked on marker', async () => {
    const marker = new MapMarker(
      Pages.hotelsResults.railMap.getMarkers().last()
    );
    
    await marker.click();
    const result = await HotelResult.findFromMapMarker(marker);
    expect(result.elm.isPresent()).eventually.to.be.true;
  });
  
  it('should open provider page when "View Deal" is clicked', async () => {
    const hotelSearchResult = Pages.hotelsResults.getExpandedSearchResult(0);
    await hotelSearchResult.viewDeal();
    
    const windows = await browser.driver.getAllWindowHandles();
    expect(windows.length).to.equal(2);
  });
  
});
