import { browser } from "protractor";
import { expect, use } from "chai";
import chaiAsPromised from "chai-as-promised";
import { Kayak } from "../pages/Kayak";
import { Hotels } from "../pages/Hotels";
import { HotelsResults } from "../pages/HotelsResults";
import { MapMarker } from "../elements/MapMarker";
import { HotelResult } from "../elements/HotelResult";
import { TabType } from "../elements/TabType";
import { waitForElementToBeInteractive } from "../utils/browser.utils";
import { switchTabAndLoadItsContainer } from "../utils/specs.utils";

use(chaiAsPromised);

describe('Kayak.com/hotels', () => {
  const kayakPage = new Kayak();
  const hotelsPage = new Hotels();
  const hotelsResultsPage = new HotelsResults();
  
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(done)
  });
  
  it('should open kayak.com', async () => {
    const url = 'https://www.kayak.com';
    browser.get(url);
    expect(browser.getCurrentUrl()).eventually.to.contain(url);
  });
  
  it('should click "Hotels" on navigation bar', () => {
    kayakPage.navigation.to('hotels');
    expect(browser.getCurrentUrl()).eventually.to.equal('https://www.kayak.com/hotels');
    expect(hotelsPage.destination.getDisplayField().isPresent()).eventually.to.be.true;
  });
  
  it('should show "1 room, 2 guests" in guests field"', () => {
    expect(hotelsPage.travellers.getDisplayText()).eventually.to.equal('1 room, 2 guests');
  });
  
  it('should have start-date field', () => {
    expect(hotelsPage.dateRange.getStartDateElement().isPresent()).eventually.to.be.true;
  });
  
  it('should have end-date field', () => {
    expect(hotelsPage.dateRange.getEndDateElement().isPresent()).eventually.to.be.true;
  });
  
  it('should load hotels results for search string NYC', async () => {
    hotelsPage.destination.getDisplayField().click();
    await waitForElementToBeInteractive(hotelsPage.destination.getInputField());
    hotelsPage.destination.getInputField().sendKeys('NYC');
    await hotelsPage.destination.selectSearchResult(0);
    hotelsPage.clickSearch();
    await hotelsResultsPage.load();
    expect(hotelsResultsPage.getSearchResults().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should display at least 5 search results', () => {
    expect(hotelsResultsPage.getSearchResults().count()).eventually.to.be.gte(5);
  });
  
  it('should open details of first search result', async () => {
    const searchResult = hotelsResultsPage.getSearchResult(0);
    searchResult.openTabs();
    expect(searchResult.getTabsContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should display hotel images in "Details" section', async () => {
    const searchResult = hotelsResultsPage.getSearchResult(0);
    expect(searchResult.getHotelImages().count()).eventually.to.be.greaterThan(0);
  });
  
  it('should switch to "Map" tab', async () => {
    const searchResult = hotelsResultsPage.getSearchResult(0);
    await switchTabAndLoadItsContainer(searchResult, TabType.MAP);
    await waitForElementToBeInteractive(searchResult.getHotelMap());
    expect(searchResult.getHotelMap().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Reviews" tab', async () => {
    const searchResult = hotelsResultsPage.getSearchResult(0);
    await switchTabAndLoadItsContainer(searchResult, TabType.REVIEWS);
    await waitForElementToBeInteractive(searchResult.getHotelReviews());
    expect(searchResult.getHotelReviews().isDisplayed()).eventually.to.be.true;
  });
  
  it('should switch to "Rates" tab', async () => {
    const searchResult = hotelsResultsPage.getSearchResult(0);
    await switchTabAndLoadItsContainer(searchResult, TabType.RATES);
    await waitForElementToBeInteractive(searchResult.getHotelRates());
    expect(searchResult.getHotelRates().isDisplayed()).eventually.to.be.true;
  });
  
  it('should open "map view" ', async () => {
    await hotelsResultsPage.railMap.show();
    await waitForElementToBeInteractive(hotelsResultsPage.railMap.getContainer());
    expect(hotelsResultsPage.railMap.getContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should show horizontal filters', () => {
    expect(hotelsResultsPage.getHorizontalFiltersContainer().isDisplayed()).eventually.to.be.true;
  });
  
  it('should show map marker details when mouse hovered', async () => {
    const markers = hotelsResultsPage.railMap.getMarkers();
    const marker = new MapMarker(markers.last());
    await marker.hoverMouse();
    expect(marker.isSummaryCardDisplayed(), 'market details should show').eventually.to.be.true;
  });
  
  it('should open hotel card when clicked on marker', async () => {
    const marker = new MapMarker(
      hotelsResultsPage.railMap.getMarkers().last()
    );
    
    await marker.click();
    const result = await HotelResult.findFromMapMarker(marker);
    expect(result.container.isPresent()).eventually.to.be.true;
  });
  
  it('should open provider page when "View Deal" is clicked', async () => {
    const hotelSearchResult = hotelsResultsPage.getExpandedSearchResult(0);
    await hotelSearchResult.viewDeal();
    
    const windows = await browser.driver.getAllWindowHandles();
    expect(windows.length).to.equal(2);
  });
  
});
