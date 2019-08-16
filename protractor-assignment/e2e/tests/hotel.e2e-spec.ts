import { Aliases } from './../shared/constants';
import { expect } from 'chai';
import { AppHotelPage } from '../pages/hotel.po';
import { browser, protractor, element, by, $$, ElementArrayFinder, ElementFinder } from 'protractor';
import { HotelDetailPage } from '../pages/hotel-detail.po';

describe('kayak user', () => {
  browser.manage().window().maximize();
  browser.ignoreSynchronization = true;
  let page : AppHotelPage;
  before(() => {
    page = new AppHotelPage();
    browser.waitForAngularEnabled(false);
    page.navigateTo();
    page.getHotelLink().click();
  });
  it('should click the hotel button and navigate to hotels page', () => {
    browser.getCurrentUrl().then(( currentUrl : string) => {
      expect(currentUrl).to.equal(`${browser.baseUrl}/hotels`);
      // tslint:disable-next-line: no-unused-expression
      expect(page.getOriginInput()).to.be.exist;
      // tslint:disable-next-line: no-unused-expression
      expect(page.getStartDate()).to.be.exist;
      // tslint:disable-next-line: no-unused-expression
      expect(page.getEndDate()).to.be.exist;
      page.getDisplayText().getText().then(( text : string) => {
        expect(text).to.equal(Aliases.guestFieldText);
      });
    });
  });

});


describe('kayak user', () => {
  browser.manage().window().maximize();
  browser.ignoreSynchronization = true;
  let page : AppHotelPage;
  let  detailPage : HotelDetailPage ;
  before(async () => {
    page = new AppHotelPage();
    detailPage = new HotelDetailPage();
    browser.waitForAngularEnabled(false);
    page.navigateToHotel();
  });

  it('should click the origin field', async () => {
    await page.getOriginInputWrapper().click();
    await page.getOriginInput().sendKeys(Aliases.originSearchKeywork);
    searchTriggersHandler(page.getOriginDropdown());
    page.getOriginDropdown().click();
    page.getSearchButton().click();
    browser.sleep(11000);
    const divLists : ElementArrayFinder = element.all(by.css('[id$=searchResultsList] .normalResults div[tabindex]'));
    const count : number = await divLists.count();
    expect(count).to.greaterThan(4);
  });
  it('should click the hotel link', async () => {
    await detailPage.getHotelDetailLink().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await detailPage.getHotelDetailSection().isDisplayed()).to.be.true;
    // tslint:disable-next-line: no-unused-expression
    expect(await detailPage.getHotelImages().isDisplayed()).to.be.true;
  });
  it('should click the map tab', async () => {
    await detailPage.getMapTabLink().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await detailPage.getMapSection().isDisplayed()).to.be.true;
  });
  it('should click the review tab', async () => {
    await detailPage.getReviewTabLink().first().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await detailPage.getReviewsSection().isDisplayed()).to.be.true;
  });
  it('should click the rates tab', async () => {
    await detailPage.getratesTabLInk().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await detailPage.getRatesSection().isDisplayed()).to.be.true;
  });
  it('should click go to map', async () => {
    searchTriggersHandler(detailPage.getGoToMapLink());
    await detailPage.getGoToMapLink().click();
    expect(await detailPage.getGoToMapSection().getAttribute('class')).to.contain('open');
  });
  async function searchTriggersHandler ( ele : ElementFinder) : Promise<void> {
    const expectedCondition = protractor.ExpectedConditions;
    const clickable = expectedCondition.elementToBeClickable(ele);
    browser.wait(clickable, 5000);
  }
});
