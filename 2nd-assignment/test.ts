import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();

let homePageObject: HomePageObject = new HomePageObject();

describe("kayak Automation", async function() {
  before(function() {
    browser.waitForAngularEnabled(false);
    browser.get(homePageObject.url);
    homePageObject.clearCookies();
  });

  it("Should display the title of momondo", async function() {
    await homePageObject.title.getText().should.eventually.be.equal("Buche günstige Flüge mit dem momondo-Flugvergleich");
  });

  it("should display the 'Travel Inspiration' section", async function() {
    await homePageObject.displayTravelInspirationSection().should.eventually.be.equal(true);
  });

  it("should display the 'Trending Cities' section", async function() {
    await homePageObject.displayTrendingCitiesSection().should.eventually.be.equal(true);
  });

  it("should display the 'Trending Countries' section", async function() {
    await homePageObject.displayTrendingCountriesSection().should.eventually.be.equal(true);
  });

  it("Should display at least 2 tiles under 'Travel Inspiration' ", async function() {
    await homePageObject.getTilesInTravelInspiration().should.eventually.be.equal(true);
  });

  it("Should display at least 20 tiles under 'Trending Cities' ", async function() {
    await homePageObject.getTrendingCityTiles().should.eventually.be.equal(true);
  });

  it("Should display at least 20 tiles under 'Trending Countries' ", async function() {
    await homePageObject.getTrendingCountriesTiles().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Travel Inspiration'", async function() {
    await homePageObject.getTravelInspirationFirstImage().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Trending Cities'", async function() {
    await homePageObject.citiesFirstImage.isDisplayed().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Trending Countries'", async function() {
    await homePageObject.countriesFirstImage.isDisplayed().should.eventually.be.equal(true);
  });

  it("Should be able to click the first tile under 'Travel Inspiration' section", async function() {
    ((await homePageObject.clickFirstTravelInspirationTile()).toString()).should.includes('nachhaltigere-fluege-finden');
  });

  it("Should be able to click 'More Inspiration' button  under 'Travel Inspiration' section", async function() {
    ((await homePageObject.clickMoreInspirationButton()).toString()).should.includes('entdecken');
  });

  it("Should be able to click the 1st tile under 'Trending Cities' section", async function() {
    ((await homePageObject.clickFirstCityTile()).toString()).should.includes('palma-de-mallorca');
  });

  it("Should be able to click the 1st tile under 'Trending Countries' section", async function() {
    ((await homePageObject.clickFirstCountryTile()).toString()).should.includes('usa');
  });
});
