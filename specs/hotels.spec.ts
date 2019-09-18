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
    expect(hotelsPage.destination.getDialog().isPresent()).eventually.to.be.true;
  });
  
  it('should show "1 room, 2 guests" in guests field"', () => {
    expect(Pages.hotels.travellers.getDisplayText()).eventually.to.equal('1 room, 2 guests');
  });
  
  it('should have start-date field', () => {
    expect(Pages.hotels.dateRange.getStartDateElement().isPresent()).eventually.to.be.true;
  });
  
  it('should have end-date field', () => {
    expect(Pages.hotels.dateRange.getEndDateElement().isPresent()).eventually.to.be.true;
  });
  
  it('should load hotels results for search string NYC', async () => {
    Pages.hotels.destination.type('NYC');
    Pages.hotels.destination.selectSearchResult(0);
    Pages.hotels.clickSearch();
    await Pages.hotelsResults.load();
    expect(Pages.hotelsResults.getSearchResults().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should display at least 5 search results', () => {
    expect(Pages.hotelsResults.getSearchResults().count()).eventually.to.be.gte(5);
  });
  
  it('should open details of first search result', async () => {
    const resultsPage = Pages.hotelsResults;
    const searchResult = resultsPage.getSearchResult(0);
    searchResult.openTabs();
    expect(searchResult.getTabsContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should display hotel images in "Details" section', async () => {
    const searchResult = Pages.hotelsResults.getSearchResult(0);
    expect(searchResult.getHotelImages().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should switch to "Map" tab', async () => {
    const searchResult = Pages.hotelsResults.getSearchResult(0);
    searchResult.switchToTab('Map');
    expect(searchResult.getHotelMap().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Reviews" tab', async () => {
    const searchResult = Pages.hotelsResults.getSearchResult(0);
    searchResult.switchToTab('Reviews');
    expect(searchResult.getHotelReviews().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Rates" tab', async () => {
    const searchResult = Pages.hotelsResults.getSearchResult(0);
    searchResult.switchToTab('Rates');
    expect(searchResult.getHotelRates().isDisplayed()).eventually.to.be.true;
  });
  
  it('should open "map view" ', () => {
    const resultsPage = Pages.hotelsResults;
    resultsPage.railMap.show();
    expect(resultsPage.railMap.getContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should show horizontal filters', () => {
    expect(Pages.hotelsResults.getHorizontalFiltersContainer().isDisplayed()).eventually.to.be.true;
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
