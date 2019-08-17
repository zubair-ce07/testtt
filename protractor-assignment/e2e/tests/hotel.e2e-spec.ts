import { Aliases } from './../shared/constants';
import { expect } from 'chai';
import { AppHotelPage } from '../pages/hotel.po';
import { browser, element, by, ElementArrayFinder } from 'protractor';
import { HotelDetailPage } from '../pages/hotel-detail.po';
import { browserWaitHandler } from '../shared/utils';

describe('kayak app assignment', () => {
  let hotelPage : AppHotelPage;
  let hotelDetailPage : HotelDetailPage;
  before(() => {
    hotelPage = new AppHotelPage();
    browser.waitForAngularEnabled(false);
    hotelPage.navigateTo();
  });
  it.only('home page should navigate & verify hotel page', async () => {
    hotelPage.getHotelLink().click();
    const currentUrl = await browser.getCurrentUrl();
    expect(currentUrl).to.equal(`${browser.baseUrl}/hotels`);
    expect(await hotelPage.getHotelOriginContainerWrapper().isDisplayed()).to.be.true;
    expect(await hotelPage.getStartDate().isDisplayed()).to.be.true;
    expect(await hotelPage.getEndDate().isDisplayed()).to.be.true;
  });

  context('hotel page', () => {
    before(async () => {
      hotelPage.navigateToHotel();
    });

    it('should click the origin field', async () => {
      await hotelPage.getOriginInputWrapper().click();
      await hotelPage.getOriginInput().sendKeys(Aliases.originSearchKeywork);
      await browserWaitHandler(hotelPage.getOriginDropdown());
      hotelPage.getOriginDropdown().click();
      hotelPage.getSearchButton().click();
      browser.sleep(11000);
      const hotelResultList : ElementArrayFinder = hotelPage.getSearchResultsList();
      const hotelResultCount : number = await hotelResultList.count();
      expect(hotelResultCount).to.greaterThan(4);
    });
    it('should click the hotel link', async () => {
      await hotelDetailPage.getHotelDetailLink().click();
      expect(await hotelDetailPage.getHotelDetailSection().isDisplayed()).to.be.true;
      expect(await hotelDetailPage.getHotelImages().isDisplayed()).to.be.true;
    });
    it('should click the map tab', async () => {
      await hotelDetailPage.getMapTabLink().click();
      expect(await hotelDetailPage.getMapSection().isDisplayed()).to.be.true;
    });
    it('should click the review tab', async () => {
      await hotelDetailPage.getReviewTabLink().click();
      expect(await hotelDetailPage.getReviewsSection().isDisplayed()).to.be.true;
    });
    it('should click the rates tab', async () => {
      await hotelDetailPage.getratesTabLInk().click();
      expect(await hotelDetailPage.getRatesSection().isDisplayed()).to.be.true;
    });
  });

  context('hotel search result page', () => {
    before(async () => {
      hotelPage = new AppHotelPage();
      hotelDetailPage = new HotelDetailPage();
      browser.waitForAngularEnabled(false);
      hotelPage.navigateToHotel();
      await hotelPage.getOriginInputWrapper().click();
      await hotelPage.getOriginInput().sendKeys(Aliases.originSearchKeywork);
      browserWaitHandler(hotelPage.getOriginDropdown());
      hotelPage.getOriginDropdown().click();
      hotelPage.getSearchButton().click();
      browser.sleep(5000);
      browserWaitHandler(hotelDetailPage.getGoToMapLink());
      await hotelDetailPage.getGoToMapLink().click();
    });
    it('should show the map section', async () => {
      expect(await hotelDetailPage.getGoToMapSection().getAttribute('class')).to.contain('open');
    });
    it('should hover the hotel marker and display summary section', async () => {
      browserWaitHandler(hotelDetailPage.getAllHotelMarkers().get(0));
      await browser.actions().mouseMove(hotelDetailPage.getAllHotelMarkers().get(0)).perform();
      expect(await element(by.css('[id*=summaryCard]')).isDisplayed()).to.be.true;
    });
    it('should click the hotel marker , click the view deal button', async () => {
      browserWaitHandler(hotelDetailPage.getAllHotelMarkers().get(0));
      await hotelDetailPage.getAllHotelMarkers().get(0).click();
      const markerId = await hotelDetailPage.getAllHotelMarkers().get(0).getAttribute('id');
      const markerIdSuffix = markerId.split('-')[1];
      expect(await element(by.id(markerIdSuffix)).isDisplayed()).to.be.true;
      const viewDealBtnId = `${markerIdSuffix}-booking-bookButton`;
      const btn = await hotelDetailPage.getViewDealButton(viewDealBtnId).click();
      browser.sleep(10000);
      const handlers = await browser.getAllWindowHandles();
      browser.switchTo().window(handlers[1]);
      expect(await browser.getCurrentUrl()).contains(Aliases.hotelsBaseUrl);
    });
  });

});
