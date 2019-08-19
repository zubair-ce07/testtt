import { Aliases } from './../shared/constants';
import { expect } from 'chai';
import { AppHotelPage } from '../pages/hotel.po';
import { browser, element, by } from 'protractor';
import { HotelDetailPage } from '../pages/hotel-detail.po';
import { browserWaitHandler } from '../shared/utils';

describe('kayak app assignment', () => {
  let hotelPage : AppHotelPage;
  let hotelDetailPage : HotelDetailPage;
  before(() => {
    hotelPage = new AppHotelPage();
    hotelDetailPage = new HotelDetailPage();
    hotelPage.navigateTo();
    hotelPage.getHotelLink().click();
  });
  it('home page should navigate & verify hotel page', async () => {
    const currentUrl = await browser.getCurrentUrl();
    expect(currentUrl).to.equal(`${browser.baseUrl}/hotels`);
  });
  it('should display destination origin field', async () => {
    expect(await hotelPage.getHotelOriginContainerWrapper().isDisplayed()).to.be.true;
  });
  it('should display departing field', async () => {
    expect(await hotelPage.getStartDate().isDisplayed()).to.be.true;
  });
  it('should display returning field', async () => {
    expect(await hotelPage.getEndDate().isDisplayed()).to.be.true;
  });

  context('hotel page', () => {
    let hotelResultCount : number;
    before(async () => {
      hotelResultCount = await hotelPage.getSearchHotelHandler();
      await hotelDetailPage.getHotelDetailLink().click();
    });
    it('should select the destination field', async () => {
      expect(hotelResultCount).to.greaterThan(4);
    });
    it('should click the hotel link and display detail and images section', async () => {
      expect(
        await hotelDetailPage.getHotelDetailSection().isDisplayed() &&
        await hotelDetailPage.getHotelImages().isDisplayed()).to.be.true;
    });
    it('should click the map tab and display map section', async () => {
      await hotelDetailPage.getMapTabLink().click();
      expect(await hotelDetailPage.getMapSection().isDisplayed()).to.be.true;
    });
    it('should click the review tab and display review section', async () => {
      await hotelDetailPage.getReviewTabLink().click();
      expect(await hotelDetailPage.getReviewsSection().isDisplayed()).to.be.true;
    });
    it('should click the rates tab and display rates section', async () => {
      await hotelDetailPage.getratesTabLInk().click();
      expect(await hotelDetailPage.getRatesSection().isDisplayed()).to.be.true;
    });
  });

  context('hotel search result page', () => {
    before(async () => {
      await hotelPage.getSearchHotelHandler();
      await hotelDetailPage.getHotelDetailLink().click();
      browserWaitHandler(hotelDetailPage.getGoToMapLink());
      await hotelDetailPage.getGoToMapLink().click();
    });
    it('should show the map section', async () => {
      expect(await hotelDetailPage.getGoToMapSection().getAttribute('class')).to.contain('open');
    });
    it('should hover the hotel marker and display summary section', async () => {
      browserWaitHandler(hotelDetailPage.getAllHotelMarkers().get(0));
      await browser.actions().mouseMove(hotelDetailPage.getAllHotelMarkers().get(0)).perform();
      expect(await hotelDetailPage.getMarkerSummary().isDisplayed()).to.be.true;
    });
    it('should click the hotel marker and display hotel card', async () => {
      const markerIdSuffix =  await  hotelDetailPage.getHotelMarkerId();
      expect(await element(by.id(markerIdSuffix)).isDisplayed()).to.be.true;
    });
    it('should click the view deal button and open provider page in new tab', async () => {
      await hotelDetailPage.getViewDealBUttonId();
      expect(await browser.getCurrentUrl()).contains(Aliases.hotelsBaseUrl);
    });
  });
});
