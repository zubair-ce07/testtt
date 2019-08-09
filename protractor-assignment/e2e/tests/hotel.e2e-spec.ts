import { Aliases } from './../shared/constants';
import { expect } from 'chai';
import { AppHotelPage } from '../pages/hotel.po';
import { browser, protractor, element, by, $$, ElementArrayFinder, ElementFinder } from 'protractor';

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
  before(async () => {
    page = new AppHotelPage();
    browser.waitForAngularEnabled(false);
    page.navigateToHotel();
  });

  it('should click the origin field', async () => {
    await page.getOriginInputWrapper().click();
    await page.getOriginInput().sendKeys('BCN');
    searchTriggersHandler(page.getOriginDropdown());
    page.getOriginDropdown().click();
    page.getSearchButton().click();
    browser.sleep(11000);
    const divLists : ElementArrayFinder = element.all(by.css('[id$=searchResultsList] .normalResults div[tabindex]'));
    const count : number = await divLists.count();
    expect(count).to.greaterThan(4);
  });
  it('should click the hotel link', async () => {
    await element(by.css('.normalResults > div:nth-child(2) div.mainItemWrapper button.allowWrap')).click();
    // tslint:disable-next-line: no-unused-expression
    expect(await element.all(by.css('[id$=detailsContent] .inlineTab.active')).first().isDisplayed()).to.be.true;
    // tslint:disable-next-line: no-unused-expression
    expect(await element.all(by.css('[id$=overviewContainer] .col-photos')).first().isDisplayed()).to.be.true;
  });
  it('should click the map tab', async () => {
    await element.all(by.css('[id$=detailsContent] div[data-tab=map]')).first().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await element.all(by.css('[id$=mapContainer]')).first().isDisplayed()).to.be.true;
  });
  it('should click the review tab', async () => {
    await element.all(by.css('[id$=detailsContent] div[data-tab=reviews]')).first().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await element.all(by.css('[id$=reviewsContainer]')).first().isDisplayed()).to.be.true;
  });
  it('should click the rates tab', async () => {
    await element.all(by.css('[id$=detailsContent] div[data-tab=rates]')).first().click();
    // tslint:disable-next-line: no-unused-expression
    expect(await element.all(by.css('[id$=ratesContainer]')).first().isDisplayed()).to.be.true;
  });
  it('should click go to map', async () => {
    searchTriggersHandler(page.getGoToMapLink());
    await page.getGoToMapLink().click();
    expect(await element(by.css('[id$=rightRail] .rail-map-container > div')).getAttribute('class')).to.contain('open');
  });
  async function searchTriggersHandler ( ele : ElementFinder) : Promise<void> {
    const expectedCondition = protractor.ExpectedConditions;
    const clickable = expectedCondition.elementToBeClickable(ele);
    browser.wait(clickable, 5000);
  }
});
